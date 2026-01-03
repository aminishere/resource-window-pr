
# Resource Window Booking REST API

**Resource Window PR** is a backend system for managing resources and bookings with time-window constraints. It allows users to:

- Create, update, and cancel bookings for resources.
- Check availability of resources.
- Add resources


## Features

- User authentication with JWT  
- Resource CRUD operations  
- Booking creation, update, cancellation  
- Availability checks for resources  
- Handling concurrent booking request by row locking in database
  
## Tech Stack


<div align = 'center'>  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/tailwindcss/tailwindcss-original.svg"  width="40" height="40" />  <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/fastapi/fastapi-original.svg" width="40" height="40"  /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/sqlalchemy/sqlalchemy-original.svg" width="40" height="40" /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" width="40" height="40" /> <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azuresqldatabase/azuresqldatabase-original.svg" width="40" height="40" /> </div>

## Project Structure

resource-window-pr/  
├── .gitignore  
├── app/  
│   ├── api/  
│   │   ├── auth.py  
│   │   ├── bookings.py  
│   │   └── resources.py  
│   ├── database.py  
│   ├── main.py  
│   ├── models/  
│   │   ├── booking.py  
│   │   ├── resource.py  
│   │   └── user.py  
│   ├── schemas/  
│   │   ├── booking.py  
│   │   ├── resource.py  
│   │   └── user.py  
│   ├── scripts/  
│   │   └── seed.py  
│   ├── service/  
│   │   ├── booking_service.py  
│   │   ├── concurrent_bookings.py  
│   │   ├── conflict_detector.py  
│   │   ├── operations.py  
│   │   └── validators.py  
│   └── utils/  
│       └── security.py  
├── README.md  
└── requirements.txt  


## API Endpoints

| Method | Endpoint                    | Description                     |
|--------|-----------------------------|---------------------------------|
| POST   | `/auth/register`                    | User register                      |
| POST   | `/auth/login`                    | User login                      |
| POST   | `/resources/`               | Create a resource               |
| POST   | `/bookings/`                | Create a booking                |
| PUT    | `/bookings/{id}`            | Update a booking                |
| DELETE | `/bookings/{id}`            | Cancel a booking                |
| GET    | `/bookings/resource/{resource_id}/availability`   | Check a resource availability     |
| GET    | `/bookings/my-bookings/`       | Get current user’s bookings     |




### Authentication
All protected endpoints require a JWT token in the request header:

```http
Authorization: Bearer <token>
```

## Installation

 Clone the repository:

```bash
git clone https://github.com/aminishere/resource-window-pr.git
cd resource-window-pr
```
Create a virtual environment and activate it:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Set environment variables (create a .env file):
```bash
DATABASE_URL=postgresql://user:password@host:5432/resource-window-pr
```
Run seed script to populate database:
```bash
python -m app.scripts.seed
```

Start the server:
```bash
uvicorn app.main:app --reload
```
