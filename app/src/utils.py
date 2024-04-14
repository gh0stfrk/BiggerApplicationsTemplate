import os
from pathlib import Path
from passlib.context import CryptContext
from fastapi import UploadFile, HTTPException
from datetime import datetime, timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from .config import Config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """
    Hashes the password using bcrypt.
    """
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    """
    Verifies the password using bcrypt.
    """
    return pwd_context.verify(password, hashed_password)


def create_user_dir(username: str):
    """
    Creates a directory for the user.
    """
    try:
        user_dir = Path(Config.MEDIA_DIR) / username
        user_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating user directory: {e}")
    
def save_profile_photo(username: str, profile_photo: UploadFile):
    """
    Saves the profile photo for the user.
    """
    try:
        user_dir = Path(Config.MEDIA_DIR) / username
        profile_photo_path = user_dir / profile_photo.filename
        with open(profile_photo_path, "wb") as f:
            f.write(profile_photo.file.read())
        return profile_photo_path.parent / profile_photo.filename
    except Exception as e:
        print(f"Error saving profile photo: {e}")


def create_access_token(payload: dict, expires:timedelta = None) -> str:
    """
    Creates an access token.
    """
    to_encode = payload.copy()
    if expires: 
        expire = datetime.utcnow() + expires
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> dict:
    """
    Decodes an access token.
    """
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        return payload
    except JWTError:
        return HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    except ExpiredSignatureError:
        return HTTPException(
            status_code=401,
            detail="Token expired"
        )

def get_user_from_token(token: str, db):
    """
    Gets the user from the token.
    """
    token_data = decode_access_token(token)
    from .domain.user.models import User
    user = db.query(User).filter(User.id == token_data["id"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="User Not Found!")
    return user