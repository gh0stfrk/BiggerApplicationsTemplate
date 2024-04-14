from typing import Annotated
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ..domain.user.schema import Token
from ..domain.user.service import get_user_by_username
from ..utils import hash_password, verify_password, create_access_token
from ..dependencies import get_db


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:Session = Depends(get_db)):
    invalid_user_exception = HTTPException(status_code=400, detail="Incorrect username or password")
    user = get_user_by_username(form_data.username, db)
    if not user:
        raise invalid_user_exception
    authenticated = verify_password(form_data.password, user.password)
    if not authenticated:
        raise invalid_user_exception
    token_data = {"id": user.id, "sub": user.username}
    token = create_access_token(token_data)
    return Token(access_token=token, token_type="bearer")