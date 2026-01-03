from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.booking import Booking

def lock_and_create(
    db: Session,
    resource_id: int,
    start_time: datetime,
    end_time: datetime,
    user_id: int,
) -> Booking:
        
    #Lock rows first, then check and insert.    
    try:
        conflicts = (
            db.query(Booking)
            .filter(
                Booking.resource_id == resource_id,
                Booking.status == "confirmed",
                Booking.start_time < end_time,
                Booking.end_time > start_time,
            ).with_for_update().all()
        )

        if conflicts:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Resource is already booked")

        booking = Booking(
            user_id=user_id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            status="confirmed",
            version=0,
        )
        db.add(booking)
        db.commit()
        db.refresh(booking)
        return booking

    except HTTPException:
        db.rollback()
        raise
    except Exception:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create booking")
