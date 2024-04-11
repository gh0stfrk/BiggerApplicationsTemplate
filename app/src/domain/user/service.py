from sqlalchemy.orm import Session
from typing import List
from .models import User
from .schema import UserSchema, UserUpdate


def create_user(user: UserSchema, db: Session) -> User:
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_username(username: str, db: Session) -> User:
    return db.query(User).filter(User.username == username, User.is_deleted == False).first()

def get_user_by_id(user_id: int, db: Session) -> User:
    return db.query(User).filter(User.id == user_id, User.is_deleted == False).first()

def get_all_users(db: Session) -> List[User]:
    return db.query(User).filter(User.is_deleted == False).all()

def delete_user(user_id: int, db: Session) -> bool:
    """
    Delete User
    :param user_id: User id
    :param db: Database session
    :return: True if deleted else False
    """
    try:
        db.query(User).filter(User.id == user_id).delete()
        db.commit()
    except Exception as e:
        return False
    return True


def update_user(user_id: int, user_details: UserUpdate, db: Session) -> User | None:
    """
    Update user
    :param user_id: User id
    :param user_details: UserUpdate object
    :param db: Database session
    :return: User object if exist's else None
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for var, value in vars(user_details).items():
        if value is not None:
            setattr(user, var, value)
    db.commit()
    db.refresh(user)
    return user

def is_unique_username(username: str, db: Session) -> bool:
    """
    Check if username is unique
    :param username: Username
    :param db: Database session
    :return: True if unique else False
    """
    user = db.query(User).filter(User.username == username).first()
    if user:
        return False
    return True