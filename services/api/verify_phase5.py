"""
Phase 5 verification — in-process FastAPI TestClient (no shell, no network).
"""
import json, os
from datetime import UTC, datetime, timedelta

# JWT settings before any module import
os.environ["SECRET_KEY"] = "test-secret-for-verification"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

# ---------------------------------------------------------------------------
# Monkey-patch TinyDB to use MemoryStorage (never touches disk)
# ---------------------------------------------------------------------------
from tinydb import TinyDB
from tinydb.storages import MemoryStorage

import api.models as models
import api.services as services
import api.routers.records as records_mod

memory_db = TinyDB(storage=MemoryStorage)


def mem_users():
    return memory_db.table("users")


def mem_profiles():
    return memory_db.table("profiles")


def mem_records():
    return memory_db.table("records")


def mem_notes():
    return memory_db.table("notes")


# Patch model-level table helpers (imported as `get_users_table` etc. in models.py)
models.get_users_table = mem_users
models.get_profiles_table = mem_profiles
# Patch service-level table helpers
services.get_users_table = mem_users
services.get_profiles_table = mem_profiles
services.get_records_table = mem_records
services.get_notes_table = mem_notes
# Patch records router helpers
records_mod.get_records_table = mem_records
records_mod.get_notes_table = mem_notes

# ---------------------------------------------------------------------------
# Build app & TestClient
# ---------------------------------------------------------------------------
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)
results: list[dict] = []


def check(label: str, status: int, **extra) -> dict | None:
    entry = {"check": label, "status": status, **extra}
    results.append(entry)
    return None

# ===========================================================================
# 1. Register user — creates User + linked Profile in one operation
# ===========================================================================
resp = client.post("/users", json={
    "email": "alice@verification.invalid",
    "password": "p4ssword",
    "name": "Alice",
    "phone": "555-0100",
    "address": "Home",
})
assert resp.status_code == 201, resp.text
alice = resp.json()
alice_id = alice["user"]["id"]
check("POST /users → 201", 201, has_profile=alice["profile"]["user_id"] == alice_id)
assert "hashed_password" not in alice["user"]
assert "password" not in alice["user"]

# ===========================================================================
# 2. Login with correct credentials
# ===========================================================================
resp = client.post("/auth/login", json={"email": "alice@verification.invalid", "password": "p4ssword"})
assert resp.status_code == 200, resp.text
token = resp.json()["access_token"]
check("POST /auth/login → 200", 200, token_type=resp.json()["token_type"])

# ===========================================================================
# 3. Token decodes with correct sub and exp
# ===========================================================================
from jose import jwt
decoded = jwt.decode(token, "test-secret-for-verification", algorithms=["HS256"])
assert decoded["sub"] == alice_id
check("Token sub = user id", 200, sub=decoded["sub"], has_exp="exp" in decoded)

# ===========================================================================
# 4. GET /auth/me with copied token
# ===========================================================================
resp = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
assert resp.status_code == 200, resp.text
me = resp.json()
assert me["email"] == "alice@verification.invalid"
assert me["role"] == "user"
assert me["profile"]["user_id"] == alice_id
check("GET /auth/me → 200", 200, email=me["email"], role=me["role"])

# ===========================================================================
# 5. Protected routes without token → 401
# ===========================================================================
for path in ["/users", "/auth/me", "/profiles/me", "/records"]:
    r = client.get(path)
    assert r.status_code == 401, f"{path}: {r.status_code}"
check("Protected GET without token → 401", 401)
for path in ["/users/x", "/records/x"]:
    r = client.delete(path)
    assert r.status_code == 401
check("Protected DELETE without token → 401", 401)
r = client.put("/users/x", json={})
assert r.status_code == 401
check("Protected PUT without token → 401", 401)

# ===========================================================================
# 6. Malformed token → 401
# ===========================================================================
resp = client.get("/auth/me", headers={"Authorization": "Bearer this-is-garbage"})
assert resp.status_code == 401
check("Malformed token → 401", 401)

# ===========================================================================
# 7. Expired token → 401
# ===========================================================================
exp_payload = {"sub": alice_id, "exp": datetime.now(UTC) - timedelta(hours=1)}
expired_token = jwt.encode(exp_payload, "test-secret-for-verification", algorithm="HS256")
resp = client.get("/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
assert resp.status_code == 401
check("Expired token → 401", 401)

# ===========================================================================
# 8. Wrong password → 401, no token
# ===========================================================================
resp = client.post("/auth/login", json={"email": "alice@verification.invalid", "password": "wrong"})
assert resp.status_code == 401
assert "access_token" not in resp.json()
check("Wrong password → 401", 401)

# ===========================================================================
# 9. Unknown email → 401, no token
# ===========================================================================
resp = client.post("/auth/login", json={"email": "nobody@verification.invalid", "password": "p4ssword"})
assert resp.status_code == 401
assert "access_token" not in resp.json()
check("Unknown email → 401", 401)

# ===========================================================================
# 10. 403 — wrong owner on user/profile endpoints
# ===========================================================================
resp = client.post("/users", json={"email": "bob@verification.invalid", "password": "bobpass", "name": "Bob"})
bob_id = resp.json()["user"]["id"]
bob_token = client.post("/auth/login", json={"email": "bob@verification.invalid", "password": "bobpass"}).json()["access_token"]

# Bob cannot modify Alice
for method, path in [
    ("put", f"/users/{alice_id}"),
    ("delete", f"/users/{alice_id}"),
]:
    kwargs = {"headers": {"Authorization": f"Bearer {bob_token}"}}
    if method == "put":
        kwargs["json"] = {"email": "x"}
    r = getattr(client, method)(path, **kwargs)
    assert r.status_code == 403, f"{method} {path}: {r.status_code}"
check("Wrong owner user → 403", 403)

# Bob cannot access Alice's profile
r = client.get(f"/profiles/me?user_id={alice_id}", headers={"Authorization": f"Bearer {bob_token}"})
assert r.status_code == 403
r = client.put(f"/profiles/me?user_id={alice_id}", json={"name": "Hacker"}, headers={"Authorization": f"Bearer {bob_token}"})
assert r.status_code == 403
check("Wrong owner profile → 403", 403)

# ===========================================================================
# 11. Alice uses own token successfully
# ===========================================================================
r = client.get("/users", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("GET /users own token → 200", 200)

r = client.get(f"/users/{alice_id}", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("GET /users/{id} own token → 200", 200)

r = client.put(f"/users/{alice_id}", json={"is_active": False}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("PUT /users/{id} own token → 200", 200)

r = client.get("/profiles/me", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("GET /profiles/me own token → 200", 200)

r = client.put("/profiles/me", json={"phone": "555-0200"}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("PUT /profiles/me own token → 200", 200)

# ===========================================================================
# 12. Records CRUD
# ===========================================================================
r = client.post("/records", json={
    "full_name": "Candidate", "email": "c@v.invalid", "phone": "1",
    "position": "E", "status": "received", "stage": "pending", "experience_years": 2,
}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 201, r.text
rec_id = r.json()["id"]
check("POST /records → 201", 201)

r = client.get("/records", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200 and len(r.json()["data"]) == 1
check("GET /records → 200", 200)

r = client.get(f"/records/{rec_id}", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("GET /records/{id} → 200", 200)

r = client.put(f"/records/{rec_id}", json={"position": "Senior"}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("PUT /records/{id} → 200", 200)

r = client.patch(f"/records/{rec_id}", json={"status": "in_progress"}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("PATCH /records/{id} → 200", 200)

r = client.post(f"/records/{rec_id}/notes", json={"content": "Great"}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 201
note_id = r.json()["id"]
check("POST /records/{id}/notes → 201", 201)

r = client.get(f"/records/{rec_id}/notes", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200 and len(r.json()["data"]) == 1
check("GET /records/{id}/notes → 200", 200)

r = client.delete(f"/records/{rec_id}/notes/{note_id}", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 204
check("DELETE /records/{id}/notes/{id} → 204", 204)

r = client.delete(f"/records/{rec_id}", headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 204
check("DELETE /records/{id} → 204", 204)

# Records without token → 401
for path in ["/records", "/records/x", "/records/x/notes"]:
    assert client.get(path).status_code == 401
check("Records no token → 401", 401)

# ===========================================================================
# 13. TinyDB shape from memory
# ===========================================================================
u = list(mem_users().all())
assert len(u) == 2
p = list(mem_profiles().all())
assert len(p) == 2
check("TinyDB shape",
      200,
      user_fields=sorted(u[0].keys()),
      profile_fields=sorted(p[0].keys()),
      password_absent="password" not in u[0],
      hash_present="hashed_password" in u[0])

# ===========================================================================
# 14. Invalid role rejected
# ===========================================================================
r = client.put(f"/users/{bob_id}", json={"role": "owner"}, headers={"Authorization": f"Bearer {bob_token}"})
assert r.status_code == 422
check("Invalid role → 422", 422)

# ===========================================================================
# 15. Admin can cross-access
# ===========================================================================
r = client.put(f"/users/{alice_id}", json={"role": "admin"}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
r = client.put(f"/users/{bob_id}", json={"email": "bob-new@v.invalid"}, headers={"Authorization": f"Bearer {token}"})
assert r.status_code == 200
check("Admin modifies other user → 200", 200)

# ===========================================================================
# Summary
# ===========================================================================
print("ALL CHECKS PASSED")
print(json.dumps(results, indent=2))
print("\n--- Expected auth failures (401/403/422) ---")
for r in results:
    if r["status"] in (401, 403, 422):
        print(f'  ✓ {r["check"]}')

