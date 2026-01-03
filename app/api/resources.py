from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.resource import ResourceCreate, ResourceOut
from app.models.user import User
from app.models.resource import Resource
from app.database import get_db
from app.utils.security import get_current_user

router = APIRouter(prefix="/resources", tags=["resources"])

@router.post("/", response_model=ResourceOut, status_code=status.HTTP_201_CREATED)
def create_resource( payload: ResourceCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    existing = db.query(Resource).filter(Resource.name == payload.name).first()
    if existing:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=f"Resource with name '{payload.name}' already exists.")

    resource = Resource(**payload.model_dump())
    db.add(resource)
    db.commit()
    db.refresh(resource)
    return resource
