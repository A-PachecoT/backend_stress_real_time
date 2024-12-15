from fastapi import APIRouter

from app.api.endpoints import auth, questionnaire, stress_analysis, users

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(questionnaire.router)
api_router.include_router(stress_analysis.router)
