# app/schemas/booking.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BookingCreate(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime


class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None


class BookingOut(BaseModel):
    id: int
    user_id: int
    resource_id: int
    start_time: datetime
    end_time: datetime
    status: str
    version: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AvailabilitySlot(BaseModel):
    resource_id: int
    start_time: datetime
    end_time: datetime
    available: bool
