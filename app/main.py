from fastapi import APIRouter, FastAPI

from app.api.api_v1 import api
from app.core.settings import settings

from .pre_init import pre_init


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/api/{settings.API_V1_STR}/openapi.json",
)

api_v1_router = APIRouter(prefix=f"/api/{settings.API_V1_STR}")
api_v1_router.include_router(api.router)


@api_v1_router.get("/healthcheck", tags=["service"])
async def healthcheck() -> int:
    return 1


app.include_router(api_v1_router)


@app.on_event("startup")
async def startup_event():
    pre_init()
