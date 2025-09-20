from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/user", tags=["user"])

class Profile(BaseModel):
    name: str
    email: str
    age: str
    gender: str
    education: str
    boardScores: str
    grades: str
    examResults: str
    interests: list[str]

profiles = {}

@router.post("/profile")
def save_profile(profile: Profile):
    profiles[profile.email] = profile.dict()
    return {"message": "Profile saved", "profile": profile}
