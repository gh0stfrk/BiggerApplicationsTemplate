from fastapi import APIRouter
from . import user

router = APIRouter(
    prefix="/api"
)

def include_routers():
    router.include_router(user.router)
    
include_routers()