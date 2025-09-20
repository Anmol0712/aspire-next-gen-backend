from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/job_role_skills", tags=["job_role_skills"])


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Get all job-role-skill mappings
# --------------------------
@router.get("/", response_model=list[schemas.JobRoleSkillOut])
def read_job_role_skills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_job_role_skills(db, skip=skip, limit=limit)


# --------------------------
# Create new mapping
# --------------------------
@router.post("/", response_model=schemas.JobRoleSkillOut)
def create_new_mapping(mapping: schemas.JobRoleSkillCreate, db: Session = Depends(get_db)):
    return crud.create_job_role_skill(db, mapping)


# --------------------------
# Delete mapping
# --------------------------
@router.delete("/{mapping_id}", response_model=schemas.JobRoleSkillOut)
def delete_mapping(mapping_id: int, db: Session = Depends(get_db)):
    db_mapping = crud.delete_job_role_skill(db, mapping_id)
    if not db_mapping:
        raise HTTPException(status_code=404, detail="Mapping not found")
    return db_mapping
