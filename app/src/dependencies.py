from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

from .database import SessionLocal
from .utils import decode_access_token
from .domain.user.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_db():
    """ Create a database session """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def validate_token(token: str = Depends(oauth2_scheme)) -> bool:
    """ Validate Token """
    token_status = decode_access_token(token)
    return True if token_status else False

def get_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """ Get User from Token """
    token_status = decode_access_token(token)
    from .utils import get_user_from_token
    user = get_user_from_token(token, db)
    return user