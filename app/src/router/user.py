from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..domain.user.service import(
    get_all_users, 
    get_user_by_id,
    create_user,
    is_unique_username
)

from ..domain.user.schema import (
    UserSchema,
    UserUpdate,
    UserResponse
)

router = APIRouter(
    prefix="/user",
    tags=["user"]
)


@router.get("/", response_model=List[UserResponse], status_code=200)
async def get_users(db: Session = Depends(get_db)):
    users = get_all_users(db)
    return users

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
async def get_user_by_id_(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user.__dict__)

@router.post("/", response_model=UserResponse, status_code=201)
async def create_user_(user: UserSchema, db: Session = Depends(get_db)):
    if not is_unique_username(user.username, db):
        raise HTTPException(status_code=400, detail="Username already exists")
    created_user = create_user(user, db)
    return UserResponse(**created_user.__dict__)