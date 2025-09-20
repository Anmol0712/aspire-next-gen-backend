from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/domains", tags=['domains'])

# Dependency to get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------
# Get all domains
# --------------------------
@router.get("/", response_model=list[schemas.DomainOut])
def read_domains(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_domains(db, skip=skip, limit=limit)


# --------------------------
# Get single domain by ID
# --------------------------
@router.get("/{domain_id}", response_model=schemas.DomainOut)
def read_domain(domain_id: int, db: Session = Depends(get_db)):
    db_domain = db.query(crud.models.Domain).filter(crud.models.Domain.domain_id == domain_id).first()
    if not db_domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain


# --------------------------
# Create new domain
# --------------------------
@router.post("/", response_model=schemas.DomainOut)
def create_new_domain(domain: schemas.DomainCreate, db: Session = Depends(get_db)):
    return crud.create_domain(db, domain)


# --------------------------
# Update domain
# --------------------------
@router.put("/{domain_id}", response_model=schemas.DomainOut)
def update_domain(domain_id: int, domain: schemas.DomainUpdate, db: Session = Depends(get_db)):
    db_domain = crud.update_domain(db, domain_id, domain)
    if not db_domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain


# --------------------------
# Delete domain
# --------------------------
@router.delete("/{domain_id}", response_model=schemas.DomainOut)
def delete_domain(domain_id: int, db: Session = Depends(get_db)):
    db_domain = crud.delete_domain(db, domain_id)
    if not db_domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return db_domain
