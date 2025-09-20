from fastapi import FastAPI
from . import models, database

from .routers import domains, skills, job_roles, job_role_skills, branch, tests, recommendations


# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title='AspireNextGen API')

# --------------------------
# Include Routers
# --------------------------
app.include_router(domains.router)
app.include_router(skills.router)
app.include_router(job_roles.router)
app.include_router(job_role_skills.router)
app.include_router(branch.router)
app.include_router(tests.router)
app.include_router(recommendations.router)

# ---------------------------------------------------
# CORS + Dummy Auth
# ---------------------------------------------------
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in production, restrict to frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dummy user storage
users = {}

class UserSignup(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserProfile(BaseModel):
    name: str
    email: str
    age: int
    gender: str
    education: str
    boardScores: str
    grades: str
    examResults: str
    interests: list

@app.post("/auth/signup")
async def signup(user: UserSignup):
    users[user.email] = {"name": user.name, "password": user.password}
    return {"message": "Signup successful", "user": user}

@app.post("/auth/login")
async def login(user: UserLogin):
    if user.email in users and users[user.email]["password"] == user.password:
        return {"message": "Login successful", "name": users[user.email]["name"]}
    return JSONResponse(status_code=400, content={"error": "Invalid credentials"})

@app.post("/user/profile")
async def save_profile(profile: UserProfile):
    users[profile.email].update(profile.dict())
    return {"message": "Profile saved", "profile": profile}








from fastapi.responses import FileResponse
import os
from fastapi.staticfiles import StaticFiles

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend"))  # two levels up

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Serve static files (like logo.jpg, css, js if you add them later)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

