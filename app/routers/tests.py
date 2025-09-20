from fastapi import APIRouter
from pydantic import BaseModel
from app.ai_test_system import generate_test, evaluate_test

router = APIRouter(prefix="/tests", tags=["tests"])

class GenerateRequest(BaseModel):
    user_id: str
    category: str | None = None
    num_questions: int = 2

class EvaluateRequest(BaseModel):
    user_id: str
    test_data: dict
    user_answers: dict

@router.post("/generate")
def generate(req: GenerateRequest):
    return generate_test(req.user_id, req.category, req.num_questions)

@router.post("/evaluate")
def evaluate(req: EvaluateRequest):
    return evaluate_test(req.user_answers, req.test_data)
