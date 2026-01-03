# app/models/booking.py
from sqlalchemy import Column, Integer, DateTime, ForeignKey, Index, String
from app.database import Base
from datetime import datetime

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    # For optimistic locking
    version = Column(Integer, default=0, nullable=False)
    
    # Booking status: pending, confirmed, cancelled
    status = Column(String(20), default="confirmed", nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    __table_args__ = (
        Index(
            "ix_booking_resource_time",
            "resource_id",
            "start_time",
            "end_time",
        ),
        Index(
            "ix_booking_user_id",
            "user_id",
        ),
        Index(
            "ix_booking_status",
            "status",
        ),
    )

