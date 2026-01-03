import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  


DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL not set")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()  
    try:
        yield db          
    finally:
        db.close()        
