from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.booking import Booking
from app.service.validators import validate_booking_times
from app.service.concurrent_bookings import lock_and_create


def create_booking( db: Session, resource_id: int, start_time: datetime, end_time: datetime, user_id: int) -> Booking: #Create a booking using locking.

    validate_booking_times(start_time, end_time)
    return lock_and_create(db, resource_id, start_time, end_time, user_id)


def update_booking(db: Session, booking_id: int, user_id: int, start_time: datetime = None, end_time: datetime = None) -> Booking: #Update a booking with conflict detection using lock_and_create.

    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id,
    ).first()
    
    if not booking:
        raise HTTPException( status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    if booking.status != "confirmed":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cannot update booking with status: {booking.status}")
    
    new_start = start_time or booking.start_time
    new_end = end_time or booking.end_time
    
    validate_booking_times(new_start, new_end)
    
    booking.status = "cancelled" # Delete old booking temporarily to avoid self-conflict
    db.commit()
    
    try:
        updated_booking = lock_and_create(db, booking.resource_id, new_start, new_end, user_id)
        updated_booking.id = booking.id  # preserve original ID if needed
        updated_booking.version = booking.version + 1
        return updated_booking
    except HTTPException:
        booking.status = "confirmed" # Restore original booking if update fails
        db.commit()
        raise


def cancel_booking(db: Session, booking_id: int, user_id: int) -> Booking: #Cancel a booking (soft delete).
    booking = db.query(Booking).filter(
        Booking.id == booking_id,
        Booking.user_id == user_id,
    ).first()
    
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    
    if booking.status == "cancelled":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Booking is already cancelled")
    
    booking.status = "cancelled"
    booking.version += 1
    
    db.commit()
    db.refresh(booking)
    
    return booking


def get_resource_availability(db: Session, resource_id: int, start_time: datetime, end_time: datetime) -> list:  #Get available time slots for a resource.

    bookings = db.query(Booking).filter(
        Booking.resource_id == resource_id,
        Booking.status == "confirmed",
        Booking.start_time < end_time,
        Booking.end_time > start_time,
    ).order_by(Booking.start_time).all()
    
    slots = []
    current_time = start_time
    
    for booking in bookings:
        if current_time < booking.start_time:
            slots.append({
                "start_time": current_time,
                "end_time": booking.start_time,
                "available": True,
            })
        current_time = max(current_time, booking.end_time)
    
    if current_time < end_time:
        slots.append({
            "start_time": current_time,
            "end_time": end_time,
            "available": True,
        })
    
    return slots
