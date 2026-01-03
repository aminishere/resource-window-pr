from datetime import datetime, timedelta
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.service.booking_service import (create_booking, update_booking, cancel_booking, get_resource_availability, validate_date_range)
from app.database import get_db
from app.models.user import User
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingOut, BookingUpdate
from app.utils.security import get_current_user

router = APIRouter(prefix="/bookings", tags=["bookings"])

@router.post("/", response_model=BookingOut) # Create Booking
def book_resource( payload: BookingCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    return create_booking(
        db=db,
        resource_id=payload.resource_id,
        start_time=payload.start_time,
        end_time=payload.end_time,
        user_id=current_user.id,
    )


@router.patch("/{booking_id}", response_model=BookingOut) # Update Booking
def modify_booking( booking_id: int, payload: BookingUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    return update_booking(
        db=db,
        booking_id=booking_id,
        user_id=current_user.id,
        start_time=payload.start_time,
        end_time=payload.end_time,
    )

@router.delete("/{booking_id}", response_model=BookingOut) # Cancel Booking
def remove_booking( booking_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    return cancel_booking(
        db=db,
        booking_id=booking_id,
        user_id=current_user.id,
    )

@router.get("/resource/{resource_id}/availability") # Check Resource Availability
def check_availability(
    resource_id: int,
    start_date: datetime = Query(..., description="Start date for availability check"),
    end_date: Optional[datetime] = Query(None, description="End date (defaults to 7 days from start)"),
    db: Session = Depends(get_db),
):
    if end_date is None:
        end_date = start_date + timedelta(days=7)

    validate_date_range(start_date, end_date)

    slots = get_resource_availability(
        db=db,
        resource_id=resource_id,
        start_time=start_date,
        end_time=end_date,
    )

    return {
        "resource_id": resource_id,
        "start_date": start_date,
        "end_date": end_date,
        "available_slots": slots,
    }

@router.get("/my-bookings", response_model=List[BookingOut]) # List Current User's Bookings
def get_my_bookings(
    status: Optional[str] = Query(None, description="Filter by status: confirmed, cancelled"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    query = db.query(Booking).filter(Booking.user_id == current_user.id)

    if status:
        query = query.filter(Booking.status == status)

    bookings = query.order_by(Booking.start_time.desc()).all()
    return bookings
