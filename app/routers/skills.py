from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/skills", tags=["skills"])


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Get all skills
# --------------------------
@router.get("/", response_model=list[schemas.SkillOut])
def read_skills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_skills(db, skip=skip, limit=limit)


# --------------------------
# Create skill
# --------------------------
@router.post("/", response_model=schemas.SkillOut)
def create_new_skill(skill: schemas.SkillCreate, db: Session = Depends(get_db)):
    return crud.create_skill(db, skill)


# --------------------------
# Update skill
# --------------------------
@router.put("/{skill_id}", response_model=schemas.SkillOut)
def update_skill(skill_id: int, skill: schemas.SkillUpdate, db: Session = Depends(get_db)):
    db_skill = crud.update_skill(db, skill_id, skill)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill


# --------------------------
# Delete skill
# --------------------------
@router.delete("/{skill_id}", response_model=schemas.SkillOut)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    db_skill = crud.delete_skill(db, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return db_skill
