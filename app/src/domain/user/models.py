from sqlalchemy import Column, String, DateTime, Integer, Boolean
from datetime import datetime

from ...database import Base
from ...utils import hash_password

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now, default=datetime.now)
    
    @classmethod
    def set_password(cls, password: str):
        """
        Hash the password
        """
        cls.password = hash_password(password)
        return True