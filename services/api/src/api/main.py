from fastapi import FastAPI

from api.routers import auth, profiles, records, users

app = FastAPI(title="Brasaland API")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(records.router)