from fastapi import FastAPI

from api.routers import auth, profiles, users

app = FastAPI(title="Brasaland API")
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(profiles.router)