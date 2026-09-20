from fastapi import APIRouter
from app.api.v1.api import api_v1_router

api_router = APIRouter()


@api_router.get("/health", tags=["System"])
async def health_check():
    return {
        "success": True,
        "data": {
            "status": "healthy",
            "service": "AGENTX API Platform",
            "version": "0.2.0"
        },
        "error": None
    }


api_router.include_router(api_v1_router)
