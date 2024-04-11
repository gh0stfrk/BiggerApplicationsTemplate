from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy import MetaData

from ...src.database import Base
from ...src.dependencies import get_db



sqlalchemy_base_url = "sqlite:///./test.sqlite"
engine = create_engine(sqlalchemy_base_url, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def configure_test_database(app):
    app.dependency_overrides[get_db] = override_get_db
    
    from ...src.domain.user.models import User
    Base.metadata.create_all(bind=engine)


def drop_test_database():
    Base.metadata.drop_all(bind=engine)

    
def truncate_table(table_name):
    with engine.connect() as conn:
        conn.execute(text("PRAGMA ignore_check_constraints = 0"))
        conn.execute(text(f"DELETE FROM {table_name}"))
        conn.execute(text("PRAGMA ignore_check_constraints = 1"))

 
def truncate_tables(tables):
    with engine.connect() as conn:
        conn.execute(text("PRAGMA ignore_check_constraints = 0"))
        for table in tables:
            conn.execute(text(f"DELETE FROM {table}"))
        conn.execute(text("PRAGMA ignore_check_constraints = 1"))
