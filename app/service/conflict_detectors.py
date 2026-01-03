

from datetime import datetime
from sqlalchemy.orm import Session
from app.models.booking import Booking


def check_time_overlap(
    existing_start: datetime,
    existing_end: datetime,
    new_start: datetime,
    new_end: datetime,
) -> bool:
    """Check if two time ranges overlap."""
    return new_start < existing_end and new_end > existing_start


def get_conflicting_bookings(
    db: Session,
    resource_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_booking_id: int = None,
) -> list:
    """Get all confirmed bookings that conflict with the requested time."""
    query = db.query(Booking).filter(
        Booking.resource_id == resource_id,
        Booking.status == "confirmed",
        Booking.start_time < end_time,
        Booking.end_time > start_time,
    )
    
    if exclude_booking_id:
        query = query.filter(Booking.id != exclude_booking_id)
    
    return query.all()


def has_conflicts(
    db: Session,
    resource_id: int,
    start_time: datetime,
    end_time: datetime,
    exclude_booking_id: int = None,
) -> bool:
    """Check if there are any conflicting bookings."""
    conflicts = get_conflicting_bookings(
        db, resource_id, start_time, end_time, exclude_booking_id
    )
    return len(conflicts) > 0
