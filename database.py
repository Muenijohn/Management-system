from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Since trust mode is active, password can be empty or your default
DATABASE_URL = "postgresql://postgres@localhost:5432/school_supplies_db"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()