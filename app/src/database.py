import os

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


sqlalchemy_database_url = os.getenv("SQLALCHEMY_DATABASE_URL", "sqlite:///./db.sqlite")

engine = create_engine(sqlalchemy_database_url, 
                       connect_args={"check_same_thread": False})

SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()