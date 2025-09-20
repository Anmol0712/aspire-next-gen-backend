from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/job_roles", tags=["job_roles"])

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Get all job roles
# --------------------------
@router.get("/", response_model=list[schemas.JobRoleOut])
def read_job_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_job_roles(db, skip=skip, limit=limit)


# --------------------------
# Get single job role by ID
# --------------------------
@router.get("/{role_id}", response_model=schemas.JobRoleOut)
def read_job_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(crud.models.JobRole).filter(crud.models.JobRole.role_id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return db_role


# --------------------------
# Create new job role
# --------------------------
@router.post("/", response_model=schemas.JobRoleOut)
def create_new_job_role(role: schemas.JobRoleCreate, db: Session = Depends(get_db)):
    return crud.create_job_role(db, role)


# --------------------------
# Update job role
# --------------------------
@router.put("/{role_id}", response_model=schemas.JobRoleOut)
def update_job_role(role_id: int, role: schemas.JobRoleUpdate, db: Session = Depends(get_db)):
    db_role = crud.update_job_role(db, role_id, role)
    if not db_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return db_role


# --------------------------
# Delete job role
# --------------------------
@router.delete("/{role_id}", response_model=schemas.JobRoleOut)
def delete_job_role(role_id: int, db: Session = Depends(get_db)):
    db_role = crud.delete_job_role(db, role_id)
    if not db_role:
        raise HTTPException(status_code=404, detail="Job role not found")
    return db_role
