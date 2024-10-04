from fastapi import APIRouter
import settings

v1 = APIRouter(prefix=settings.API_PATH_V1)