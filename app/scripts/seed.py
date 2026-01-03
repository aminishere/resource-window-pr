from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.user import User
from app.models.resource import Resource
from app.models.booking import Booking
from app.utils.security import hash_password


def seed_users(db: Session) -> list[User]:
    users = [
        User(
            name="Admin",
            email="admin@example.com",
            password=hash_password("admin123"),
        ),
        User(
            name="User",
            email="user@example.com",
            password=hash_password("user123"),
        ),
    ]
    db.add_all(users)
    db.commit()
    for u in users:
        db.refresh(u)
    return users


def seed_resources(db: Session) -> list[Resource]:
    resources = [
        Resource(name="Conference Room A", type="room"),
        Resource(name="Conference Room B", type="room"),
        Resource(name="Projector 1", type="equipment"),
    ]
    db.add_all(resources)
    db.commit()
    for r in resources:
        db.refresh(r)
    return resources


def seed_bookings(db: Session, users: list[User], resources: list[Resource]) -> None:
    booking = Booking(
        user_id=users[0].id,
        resource_id=resources[0].id,
        start_time=datetime.now(timezone.utc) + timedelta(hours=1),
        end_time=datetime.now(timezone.utc) + timedelta(hours=2),
        status="confirmed",
        version=0,
    )
    db.add(booking)
    db.commit()


def run() -> None:
    db = SessionLocal()
    try:
        users = seed_users(db)
        resources = seed_resources(db)
        seed_bookings(db, users, resources)
        print("Seed data inserted successfully")
    finally:
        db.close()


if __name__ == "__main__":
    run()
