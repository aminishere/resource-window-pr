from datetime import datetime, timedelta, timezone, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.models.user import User
from app.database import get_db

JWT_SECRET_KEY = "secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24  

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer() # HTTP Bearer scheme

def hash_password(password: str) -> str:   
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc)  + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        
        return {"user_id": user_id}
    
    except JWTError:
        raise HTTPException( status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

def get_current_user( token_data: dict = Depends(verify_token), db: Session = Depends(get_db)) -> User:
    
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    return user
