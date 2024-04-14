from fastapi import APIRouter
from . import user, auth

router = APIRouter(
    prefix="/api"
)

def include_routers():
    router.include_router(user.router)
    router.include_router(auth.router)
    
include_routers()