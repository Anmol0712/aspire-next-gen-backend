from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/branches", tags=["branches"])


# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Get all branches
# --------------------------
@router.get("/", response_model=list[schemas.BranchOut])
def read_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_branches(db, skip=skip, limit=limit)


# --------------------------
# Create branch
# --------------------------
@router.post("/", response_model=schemas.BranchOut)
def create_new_branch(branch: schemas.BranchCreate, db: Session = Depends(get_db)):
    return crud.create_branch(db, branch)


# --------------------------
# Update branch
# --------------------------
@router.put("/{branch_id}", response_model=schemas.BranchOut)
def update_branch(branch_id: int, branch: schemas.BranchUpdate, db: Session = Depends(get_db)):
    db_branch = crud.update_branch(db, branch_id, branch)
    if not db_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return db_branch


# --------------------------
# Delete branch
# --------------------------
@router.delete("/{branch_id}", response_model=schemas.BranchOut)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    db_branch = crud.delete_branch(db, branch_id)
    if not db_branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return db_branch
