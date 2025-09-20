from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


# --------------------------
# Branch Model
# --------------------------
class Branch(Base):
    __tablename__ = "branches"

    branch_id = Column(Integer, primary_key=True, index=True)
    branch_name = Column(String(100), nullable=False, unique=True)

    domains = relationship("Domain", back_populates="branch")


# --------------------------
# Domain Model
# --------------------------
class Domain(Base):
    __tablename__ = "domains"

    domain_id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(100), nullable=False, unique=True)
    domain_description = Column(Text, nullable=True)
    branch_id = Column(Integer, ForeignKey("branches.branch_id"), index=True)

    branch = relationship("Branch", back_populates="domains")
    job_roles = relationship("JobRole", back_populates="domain")


# --------------------------
# Skill Model
# --------------------------
class Skill(Base):
    __tablename__ = "skills"

    skill_id = Column(Integer, primary_key=True, index=True)
    skill_name = Column(String(100), nullable=False, unique=True)

    job_role_links = relationship("JobRoleSkill", back_populates="skill")  # many-to-many


# --------------------------
# JobRole Model
# --------------------------
class JobRole(Base):
    __tablename__ = "job_roles"

    role_id = Column(Integer, primary_key=True, index=True)
    job_title_short = Column(String(100), nullable=False)
    domain_id = Column(Integer, ForeignKey("domains.domain_id"), index=True)
    job_description = Column(Text, nullable=True)

    domain = relationship("Domain", back_populates="job_roles")
    skill_links = relationship("JobRoleSkill", back_populates="job_role")  # many-to-many


# --------------------------
# JobRoleSkill Bridge Model
# --------------------------
class JobRoleSkill(Base):
    __tablename__ = "job_role_skills"

    role_id = Column(Integer, ForeignKey("job_roles.role_id", ondelete="CASCADE"), primary_key=True)
    skill_id = Column(Integer, ForeignKey("skills.skill_id", ondelete="CASCADE"), primary_key=True)

    job_role = relationship("JobRole", back_populates="skill_links")
    skill = relationship("Skill", back_populates="job_role_links")
