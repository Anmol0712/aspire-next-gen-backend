from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from rapidfuzz import fuzz

from app.database import get_db
from app import models
from app.schemas import RecommendationRequest
from app.summarizer import make_user_friendly_summary


router = APIRouter()

# ------------------------------
# Helpers
# ------------------------------

def _skills_lookup(db: Session):
    """Return lookup dictionaries and a list of all skills."""
    skills = db.query(models.Skill).all()
    id_to_name = {sk.skill_id: sk.skill_name for sk in skills}
    name_to_id = {sk.skill_name.lower(): sk.skill_id for sk in skills}
    all_skills = [sk.skill_name for sk in skills]
    return id_to_name, name_to_id, all_skills


def _domains_lookup(db: Session):
    """Return a list of all domains."""
    domains = db.query(models.Domain).all()
    return [d.domain for d in domains]


def fuzzy_match_domain(user_domain: Optional[str], all_domains: list[str], threshold: int = 75) -> Optional[str]:
    """
    Match user input domain to closest domain in DB using fuzzy search.
    """
    # 🔧 Debug: Check if a user domain was provided
    # print(f"[DEBUG] Domain Fuzzy Match Input: {user_domain}")

    if not user_domain:
        return None
    
    user_domain_lower = user_domain.lower().strip()
    best_match = None
    best_score = 0
    for domain in all_domains:
        score = fuzz.partial_ratio(user_domain_lower, domain.lower())
        if score > best_score and score >= threshold:
            best_match = domain
            best_score = score

    # 🔧 Debug: Print the result of the fuzzy match
    # print(f"[DEBUG] Matched Domain: {best_match} with score: {best_score}")
    return best_match


def normalize_user_skills(db: Session, user_skill_names: List[str], free_text: Optional[str]):
    """Map user-entered skills to canonical skill names/IDs using simple string matching."""
    # 🔧 Debug: Show initial user inputs
    # print(f"[DEBUG] User Skills List: {user_skill_names}")
    # print(f"[DEBUG] User Free Text: {free_text}")

    id_to_name, name_to_id, all_skills = _skills_lookup(db)

    normalized = []
    skill_ids = []

    # Process skills from the user_skill_names list with exact matching
    for s in user_skill_names:
        s_lower = s.lower()
        if s_lower in name_to_id:
            normalized.append(id_to_name[name_to_id[s_lower]])
            skill_ids.append(name_to_id[s_lower])

    # Process skills from the free_text using simple substring search
    extracted = []
    if free_text:
        free_text_lower = free_text.lower()
        for sk in all_skills:
            if sk.lower() in free_text_lower:
                extracted.append(sk)
    
    # Add extracted skills to the normalized list and get their IDs
    for ex_skill in extracted:
        if ex_skill not in normalized:
            normalized.append(ex_skill)
            if ex_skill.lower() in name_to_id:
                skill_ids.append(name_to_id[ex_skill.lower()])

    # 🔧 Debug: Show the results of the normalization
    # print(f"[DEBUG] Normalized Skills: {normalized}")
    # print(f"[DEBUG] Extracted Skills from Text: {extracted}")
    # print(f"[DEBUG] Matched Skill IDs: {skill_ids}")
    return normalized, skill_ids, extracted


def get_roles_for_skills(db: Session, skill_ids: List[int], domain_filter: Optional[str]):
    """
    Fetch roles connected to given skills, with an optional domain filter.
    Returns a list of roles, intelligently handling cases with no skills.
    """
    # # 🔧 Debug: Print parameters received
    # print(f"[DEBUG] get_roles_for_skills received skill_ids: {skill_ids}")
    # print(f"[DEBUG] get_roles_for_skills received domain_filter: {domain_filter}")

    # Fallback logic: If no skills are provided, recommend top roles based on domain preference.
    if not skill_ids:
        query = db.query(
            models.JobRole.role_id,
            models.JobRole.job_title_short,
            models.JobRole.job_description,
            models.Domain.domain,
            models.Domain.domain_description,
            models.Branch.branch_name,
            func.count(models.JobRoleSkill.skill_id).label("skill_count")
        ).join(
            models.Domain, models.Domain.domain_id == models.JobRole.domain_id
        ).join(
            models.Branch, models.Branch.branch_id == models.Domain.branch_id
        ).outerjoin(
            models.JobRoleSkill, models.JobRoleSkill.role_id == models.JobRole.role_id
        ).group_by(
            models.JobRole.role_id, models.JobRole.job_title_short, models.JobRole.job_description,
            models.Domain.domain, models.Domain.domain_description, models.Branch.branch_name
        ).order_by(
            func.count(models.JobRoleSkill.skill_id).desc()
        ).limit(5)

        if domain_filter:
            query = query.filter(models.Domain.domain.ilike(f"%{domain_filter}%"))
        
        roles = []
        for role_id, title, job_desc, domain, domain_desc, branch, _ in query.all():
            roles.append({
                "role_id": role_id,
                "job_title_short": title,
                "job_description": job_desc,
                "domain": domain,
                "domain_description": domain_desc,
                "branch": branch,
                "similarity": 0.0,
                "top_missing_skills": [],
            })
        
        # # 🔧 Debug: Show final result for fallback
        # print(f"[DEBUG] Final mapped result (Fallback): {roles}")
        return roles

    # Main logic: If skills ARE provided, proceed with the original query.
    q = (
        db.query(
            models.JobRole.role_id,
            models.JobRole.job_title_short,
            models.JobRole.job_description,
            models.Domain.domain,
            models.Domain.domain_description,
            models.Branch.branch_name,
            models.Skill.skill_id,
            models.Skill.skill_name,
        )
        .join(models.JobRoleSkill, models.JobRoleSkill.role_id == models.JobRole.role_id)
        .join(models.Skill, models.Skill.skill_id == models.JobRoleSkill.skill_id)
        .join(models.Domain, models.Domain.domain_id == models.JobRole.domain_id)
        .join(models.Branch, models.Branch.branch_id == models.Domain.branch_id)
        .filter(models.Skill.skill_id.in_(skill_ids))
    )

    if domain_filter:
        q = q.filter(models.Domain.domain.ilike(f"%{domain_filter}%"))
        
    results = q.all()
    
    roles_map: Dict[int, Dict[str, Any]] = {}
    for role_id, role_name, job_desc, domain_name, domain_desc, branch_name, skill_id, skill_name in results:
        if role_id not in roles_map:
            roles_map[role_id] = {
                "role_id": role_id,
                "job_title_short": role_name,
                "job_description": job_desc,
                "domain": domain_name,
                "domain_description": domain_desc,
                "branch": branch_name,
                "required_skills": [],
            }
        roles_map[role_id]["required_skills"].append(skill_name)
    
    final_result = list(roles_map.values())
    # # 🔧 Debug: Show final result before returning
    # print(f"[DEBUG] Final mapped result: {final_result}")

    return final_result


# ------------------------------
# API Endpoint
# ------------------------------

@router.post("/recommend")
async def recommend_endpoint(payload: RecommendationRequest, db: Session = Depends(get_db)):
    """
    Endpoint for job role recommendations with a user-friendly summary.
    """
    # 🔧 Debug: Show initial payload
    # print(f"[DEBUG] Received Payload: {payload.dict()}")
    
    normalized, skill_ids, extracted = normalize_user_skills(
        db, payload.skills, payload.free_text
    )
    
    all_domains = _domains_lookup(db)
    matched_domain = fuzzy_match_domain(payload.interest_domain, all_domains, threshold=75)

    roles = get_roles_for_skills(
        db, skill_ids, matched_domain
    )

    if skill_ids:
        for role in roles:
            all_role_skills_query = db.query(models.Skill.skill_name).join(
                models.JobRoleSkill, models.JobRoleSkill.skill_id == models.Skill.skill_id
            ).filter(models.JobRoleSkill.role_id == role["role_id"])
            all_required_skills = [s[0] for s in all_role_skills_query.all()]
            
            matched_skills = [sk for sk in all_required_skills if sk in normalized]
            missing_skills = [sk for sk in all_required_skills if sk not in normalized]
            
            similarity_score = len(matched_skills) / max(len(all_required_skills), 1)
            
            role["similarity"] = similarity_score
            role["top_missing_skills"] = missing_skills
            role["required_skills"] = all_required_skills
    
    _, _, all_skills = _skills_lookup(db)

    recommendation_data = {
        "roles": roles,
        "normalized_user_skills": normalized,
        "extract_skills_from_text": extracted,
        "recommendations_skill_gaps": {
            r["job_title_short"]: r.get("top_missing_skills", []) for r in roles
        },
        "skills_lookup": [{"skill_name": sk} for sk in all_skills],
        "domains_lookup": [{"domain": d} for d in all_domains],
        "interest_domain": matched_domain,
        "free_text": payload.free_text,
    }

    summary_text = make_user_friendly_summary(recommendation_data)
    recommendation_data["summary"] = summary_text

    # # 🔧 Debug: Show final result before returning
    # print(f"[DEBUG] Final mapped result: {recommendation_data}")

    return recommendation_data