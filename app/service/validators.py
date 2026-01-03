

from datetime import datetime
from fastapi import HTTPException, status


def validate_booking_times(start_time: datetime, end_time: datetime) -> None:
    """Validate booking start and end times."""
    if start_time >= end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be before end time",
        )
    
    if start_time < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot book in the past",
        )


def validate_date_range(start_date: datetime, end_date: datetime) -> None:
    """Validate date range for availability checks."""
    if start_date >= end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date",
        )
