from sqlalchemy.orm import Session
from . import models, schemas


# --------------------------
# Branch CRUD
# --------------------------
def create_branch(db: Session, branch: schemas.BranchCreate):
    db_branch = models.Branch(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def get_branches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Branch).offset(skip).limit(limit).all()

def update_branch(db: Session, branch_id: int, branch: schemas.BranchUpdate):
    db_branch = db.query(models.Branch).filter(models.Branch.branch_id == branch_id).first()
    if not db_branch:
        return None
    for key, value in branch.dict(exclude_unset=True).items():
        setattr(db_branch, key, value)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def delete_branch(db: Session, branch_id: int):
    db_branch = db.query(models.Branch).filter(models.Branch.branch_id == branch_id).first()
    if not db_branch:
        return None
    db.delete(db_branch)
    db.commit()
    return db_branch


# --------------------------
# Domain CRUD
# --------------------------
def create_domain(db: Session, domain: schemas.DomainCreate):
    db_domain = models.Domain(**domain.dict())
    db.add(db_domain)
    db.commit()
    db.refresh(db_domain)
    return db_domain

def get_domains(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Domain).offset(skip).limit(limit).all()

def update_domain(db: Session, domain_id: int, domain: schemas.DomainUpdate):
    db_domain = db.query(models.Domain).filter(models.Domain.domain_id == domain_id).first()
    if not db_domain:
        return None
    for key, value in domain.dict(exclude_unset=True).items():
        setattr(db_domain, key, value)
    db.commit()
    db.refresh(db_domain)
    return db_domain

def delete_domain(db: Session, domain_id: int):
    db_domain = db.query(models.Domain).filter(models.Domain.domain_id == domain_id).first()
    if not db_domain:
        return None
    db.delete(db_domain)
    db.commit()
    return db_domain


# --------------------------
# Skill CRUD
# --------------------------
def create_skill(db: Session, skill: schemas.SkillCreate):
    db_skill = models.Skill(**skill.dict())
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def get_skills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Skill).offset(skip).limit(limit).all()

def update_skill(db: Session, skill_id: int, skill: schemas.SkillUpdate):
    db_skill = db.query(models.Skill).filter(models.Skill.skill_id == skill_id).first()
    if not db_skill:
        return None
    for key, value in skill.dict(exclude_unset=True).items():
        setattr(db_skill, key, value)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def delete_skill(db: Session, skill_id: int):
    db_skill = db.query(models.Skill).filter(models.Skill.skill_id == skill_id).first()
    if not db_skill:
        return None
    db.delete(db_skill)
    db.commit()
    return db_skill


# --------------------------
# Job Role CRUD
# --------------------------
def create_job_role(db: Session, job_role: schemas.JobRoleCreate):
    db_job_role = models.JobRole(**job_role.dict())
    db.add(db_job_role)
    db.commit()
    db.refresh(db_job_role)
    return db_job_role

def get_job_roles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobRole).offset(skip).limit(limit).all()

def update_job_role(db: Session, role_id: int, job_role: schemas.JobRoleUpdate):
    db_job_role = db.query(models.JobRole).filter(models.JobRole.role_id == role_id).first()
    if not db_job_role:
        return None
    for key, value in job_role.dict(exclude_unset=True).items():
        setattr(db_job_role, key, value)
    db.commit()
    db.refresh(db_job_role)
    return db_job_role

def delete_job_role(db: Session, role_id: int):
    db_job_role = db.query(models.JobRole).filter(models.JobRole.role_id == role_id).first()
    if not db_job_role:
        return None
    db.delete(db_job_role)
    db.commit()
    return db_job_role


# --------------------------
# Job Role Skill Bridge CRUD
# --------------------------
def create_job_role_skill(db: Session, job_role_skill: schemas.JobRoleSkillCreate):
    db_jrs = models.JobRoleSkill(**job_role_skill.dict())
    db.add(db_jrs)
    db.commit()
    return db_jrs

def get_job_role_skills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.JobRoleSkill).offset(skip).limit(limit).all()

def delete_job_role_skill(db: Session, role_id: int, skill_id: int):
    db_jrs = db.query(models.JobRoleSkill).filter(
        models.JobRoleSkill.role_id == role_id,
        models.JobRoleSkill.skill_id == skill_id
    ).first()
    if not db_jrs:
        return None
    db.delete(db_jrs)
    db.commit()
    return db_jrs
