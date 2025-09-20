from pydantic import BaseModel
from typing import Optional, List, Dict

# --------------------------
# Branch Schemas
# --------------------------
class BranchBase(BaseModel):
    branch_name: str

class BranchCreate(BranchBase):
    pass

class BranchUpdate(BaseModel):
    branch_name: Optional[str] = None

class BranchOut(BranchBase):
    branch_id: int
    model_config = {"from_attributes": True}


# --------------------------
# Domain Schemas
# --------------------------
class DomainBase(BaseModel):
    domain: str
    domain_description: Optional[str] = None
    branch_id: int

class DomainCreate(DomainBase):
    pass

class DomainUpdate(BaseModel):
    domain: Optional[str] = None
    domain_description: Optional[str] = None
    branch_id: Optional[int] = None

class DomainOut(DomainBase):
    domain_id: int
    model_config = {"from_attributes": True}


# --------------------------
# Skill Schemas
# --------------------------
class SkillBase(BaseModel):
    skill_name: str

class SkillCreate(SkillBase):
    pass

class SkillUpdate(BaseModel):
    skill_name: Optional[str] = None

class SkillOut(SkillBase):
    skill_id: int
    model_config = {"from_attributes": True}


# --------------------------
# Job Role Schemas
# --------------------------
class JobRoleBase(BaseModel):
    job_title_short: str
    domain_id: int
    job_description: Optional[str] = None

class JobRoleCreate(JobRoleBase):
    pass

class JobRoleUpdate(BaseModel):
    job_title_short: Optional[str] = None
    domain_id: Optional[int] = None
    job_description: Optional[str] = None

class JobRoleOut(JobRoleBase):
    role_id: int
    model_config = {"from_attributes": True}


# --------------------------
# Job Role Skill Bridge Schemas
# --------------------------
class JobRoleSkillBase(BaseModel):
    role_id: int
    skill_id: int

class JobRoleSkillCreate(JobRoleSkillBase):
    pass

class JobRoleSkillUpdate(BaseModel):
    role_id: Optional[int] = None
    skill_id: Optional[int] = None

class JobRoleSkillOut(JobRoleSkillBase):
    model_config = {"from_attributes": True}


# --------------------------
# Recommendation Schemas
# --------------------------
class RecommendationRequest(BaseModel):
    skills: List[str] = []
    interest_domain: Optional[str] = None
    free_text: Optional[str] = None
    top_k: int = 5

class RoleRecommendation(BaseModel):
    role_id: int
    job_title_short: str
    domain: str
    branch: str
    similarity: float
    top_missing_skills: List[str]

class RecommendationResponse(BaseModel):
    roles: List[RoleRecommendation]
    normalized_user_skills: List[str]
    extract_skills_from_text: List[str]
    recommendations_skill_gaps: Dict[int, List[str]]
    summary: Optional[str] = None

    model_config = {"from_attributes": True}
 