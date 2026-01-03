# app/schemas/resource.py
from pydantic import BaseModel

class ResourceCreate(BaseModel):
    name: str
    type: str


class ResourceOut(BaseModel):
    id: int
    name: str
    type: str

    class Config:
        from_attributes = True
