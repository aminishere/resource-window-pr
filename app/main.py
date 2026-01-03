from fastapi import FastAPI, Depends
from sqlalchemy import text
from app.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.models.user import User
from app.api import auth, resources, bookings

app = FastAPI()

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Database connection successful ✅")
except Exception as e:
    print("Database connection failed ❌")
    raise e

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth.router)
app.include_router(resources.router)
app.include_router(bookings.router)