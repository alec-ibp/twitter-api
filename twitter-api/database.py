# Path
from credentials import get_database_url

# SQLAlchemy
from sqlalchemy import create_engine, engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

DATABASE_URL = ''
DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
