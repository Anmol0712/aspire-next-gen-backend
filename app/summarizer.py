import google.generativeai as genai
from typing import Dict, Any, Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API client with the API key from .env
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)


def make_user_friendly_summary(payload: Dict[str, Any]) -> str:
    """
    Build a filled prompt from the payload, send it to Gemini,
    and return a clean summary.
    """
    roles = payload.get("roles", [])
    have = payload.get("normalized_user_skills", [])
    extracted = payload.get("extract_skills_from_text", [])
    user_domain = payload.get("interest_domain")

    # --- User profile section ---
    profile_parts = []
    profile_parts.append(f"- Current Skills: {', '.join(have) if have else 'None listed'}")
    if extracted:
        profile_parts.append(f"- Skills inferred from text: {', '.join(extracted)}")
    if user_domain:
        profile_parts.append(f"- Interested Domain: {user_domain}")
    user_text = payload.get("free_text")
    if user_text and user_text.strip():
        profile_parts.append(f"- User's Note: \"{user_text.strip()}\"")
    user_profile = "\n".join(profile_parts)

    # --- Roles analysis section ---
    if roles:
        role_lines = []
        for r in roles:
            missing = r.get("top_missing_skills", [])
            missing_str = ", ".join(missing) if missing else "no major gaps detected"
            role_lines.append(
                f"- {r.get('job_title_short', 'Unknown Role')} "
                f"({r.get('domain','')}/{r.get('branch','')}) — "
                f"Match {int(r.get('similarity',0)*100)}%, Missing skills: {missing_str}"
            )
        roles_text = "\n".join(role_lines)
    else:
        roles_text = "- No roles found based on the user's current skills."

    # --- Final formatted prompt ---
    final_prompt = f"""
You are a senior career strategist AI tasked with preparing a structured career guidance report for the user.
Your response MUST follow a clear, step-wise format — do not output a single paragraph.
Write in a way that feels professional, personalized, and tailored for the user's current stage (student, undergrad, or professional).
Target length: 150–200 words total.

### USER PROFILE ###
{user_profile}

### ANALYSIS (Matching Roles & Gaps) ###
{roles_text}

### TASK ###
Write your response in *this exact format*, adapting the content to the provided user profile and role analysis.
Prioritize relevance based on the user's stage (beginner, student, working professional) and clearly justify why each skill matters.
Encourage the user to use our Roadmaps and curated content as the primary learning path.
Avoid repetitive openings like "It's fantastic that..." — keep it professional and fresh each time.
**CRITICAL INSTRUCTION: Do not mention any skills that are not explicitly listed in the "Current Skills" or "Skills inferred from text" sections of the USER PROFILE. Do not make assumptions about the user's existing knowledge or skills.**
""".strip()

    # print("=== Final Prompt Sent to Gemini ===")
    # print(final_prompt)

    # --- Call Gemini ---
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(final_prompt)
        summary = response.text.strip()
        if not summary:
            raise ValueError("Empty summary returned from Gemini")
        return summary
    except Exception as e:
        print("=== ERROR: summarization failed ===", str(e))
        return "We couldn't generate a polished summary automatically. Please try again."