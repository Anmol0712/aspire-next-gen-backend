from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

# ---- Mock User Store (replace with DB later) ----
users = {}

class SignUpRequest(BaseModel):
    name: str
    email: str
    password: str

class SignInRequest(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(req: SignUpRequest):
    if req.email in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[req.email] = {"name": req.name, "password": req.password}
    return {"message": "Signup successful", "email": req.email, "name": req.name}

@router.post("/login")
def login(req: SignInRequest):
    user = users.get(req.email)
    if not user or user["password"] != req.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "email": req.email, "name": user["name"]}
