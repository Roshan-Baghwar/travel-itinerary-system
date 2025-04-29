# Travel Itinerary System

The Travel Itinerary System is a FastAPI-based REST API for managing travel itineraries. It allows users to create custom trips, retrieve trip details, and access recommended itineraries for trips ranging from 2 to 8 nights. The system uses SQLite as the database, SQLAlchemy for ORM, and Pydantic for data validation. The application includes a seeding script to populate the database with sample data and a debugging script to inspect the database state.

## Features
- **Create Trips**: Create custom trips with specified hotels, transfers, and activities (`POST /trips`).
- **List Trips**: Retrieve all trips (`GET /trips`).
- **Get Trip Details**: Fetch a specific trip by ID (`GET /trips/{trip_id}`).
- **Recommended Itineraries**: Get pre-defined itineraries for 2–8 nights (`GET /recommend/{nights}`).
- **Database Seeding**: Populate the database with sample hotels, activities, transfers, and recommended itineraries.
- **Error Handling**: Robust validation and logging for debugging.

## Prerequisites
- **Python**: Version 3.8 or higher.
- **Git**: For cloning the repository.
- **Virtual Environment**: Recommended to isolate dependencies.
- **Dependencies**: Listed in `requirements.txt`.

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Roshan-Baghwar/travel-itinerary-system.git
   cd travel-itinerary-system
   ```

2. **Set Up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` includes:
   ```
   fastapi
   uvicorn
   sqlalchemy
   pydantic
   ```

## Running the Application
1. **Seed the Database**:
   Populate the SQLite database with sample data (hotels, activities, transfers, and recommended itineraries).
   ```bash
   python seed.py
   ```
   Expected output:
   ```
   Seeded 5 hotels
   Seeded 5 activities
   Seeded 7 itineraries
   Seeded 2 days for 2-Night Phuket & Krabi Adventure
   ...
   Database seeded successfully!
   ```

2. **Start the FastAPI Server**:
   Run the application using `uvicorn`.
   ```bash
   uvicorn main:app --reload
   ```
   If any errors running the application using `uvicorn`, use `python`.
   ```bash
   python -m uvicorn main:app --reload
   ```
   Expected output:
   ```
   INFO:     Will watch for changes in these directories: [...]
   INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
   INFO:     Started reloader process [...]
   INFO:     Started server process [...]
   INFO:     Waiting for application startup.
   INFO:     Application startup complete.
   ```

3. **Access the API**:
   The API is now running at `http://localhost:8000`. You can test endpoints using tools like `curl`, Postman, or a browser.

## Testing Instructions
The following tests verify the core functionality of the API. Use `curl` commands in a terminal to execute them while the server is running.

### 1. Verify Database State
Run the debugging script to inspect the database contents.
```bash
python check_db.py
```
**Expected Output** (partial):
```
ID: 1, Name: 2-Night Phuket & Krabi Adventure, Nights: 2, Days: 2
  Day: 2025-05-01, Hotel: 1, Transfers: [1], Activities: [1]
  ...
Transfers:
Transfer ID: 1, Day ID: 1, Description: Phuket Airport to Karon Beach
...
Trips:
No trips found in the database.
```

### 2. Test `POST /trips`
Create a new trip with a hotel, transfer, and activity.
```bash
curl -X POST http://localhost:8000/trips -H "Content-Type: application/json" -d '{
  "name": "Phuket Getaway",
  "start_date": "2025-05-01",
  "nights": 1,
  "days": [
    {
      "date": "2025-05-01",
      "hotel_id": 1,
      "transfer_ids": [1],
      "activity_ids": [1]
    }
  ]
}'
```
**Expected Output**:
```json
{
  "id": 1,
  "name": "Phuket Getaway",
  "start_date": "2025-05-01",
  "nights": 1,
  "days": [
    {
      "date": "2025-05-01",
      "hotel_id": 1,
      "transfer_ids": [6],
      "activity_ids": [1]
    }
  ]
}
```

### 3. Test `GET /trips`
List all trips in the database.
```bash
curl http://localhost:8000/trips
```
**Expected Output**:
```json
[
  {
    "id": 1,
    "name": "Phuket Getaway",
    "start_date": "2025-05-01",
    "nights": 1,
    "days": [
      {
        "date": "2025-05-01",
        "hotel_id": 1,
        "transfer_ids": [6],
        "activity_ids": [1]
      }
    ]
  }
]
```

### 4. Test `GET /trips/{trip_id}`
Retrieve the trip with ID 1.
```bash
curl http://localhost:8000/trips/1
```
**Expected Output**:
```json
{
  "id": 1,
  "name": "Phuket Getaway",
  "start_date": "2025-05-01",
  "nights": 1,
  "days": [
    {
      "date": "2025-05-01",
      "hotel_id": 1,
      "transfer_ids": [6],
      "activity_ids": [1]
    }
  ]
}
```

### 5. Test `GET /recommend/{nights}`
Get a recommended itinerary for 3 nights.
```bash
curl http://localhost:8000/recommend/3
```
**Expected Output**:
```json
{
  "id": 2,
  "name": "3-Night Phuket & Krabi Adventure",
  "start_date": "2025-05-01",
  "nights": 3,
  "days": [
    {
      "date": "2025-05-01",
      "hotel_id": 1,
      "transfer_ids": [1],
      "activity_ids": [1]
    },
    {
      "date": "2025-05-02",
      "hotel_id": 2,
      "transfer_ids": [2],
      "activity_ids": [2]
    },
    {
      "date": "2025-05-03",
      "hotel_id": 3,
      "transfer_ids": [3],
      "activity_ids": [3]
    }
  ]
}
```

## Troubleshooting
- **Database Issues**:
  - If `seed.py` fails, delete `data.db` and rerun `python seed.py`.
  - Check `check_db.py` output to verify data.
- **API Errors**:
  - Monitor `uvicorn` logs in the terminal for tracebacks.
  - Enable SQL logging by updating `database.py`:
    ```python
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
    ```
  - Test with minimal `POST /trips` request (e.g., `transfer_ids: []`) to isolate issues.
- **Validation Errors**:
  - Ensure `hotel_id`, `transfer_id`, and `activity_id` match IDs in `check_db.py` output.
- **Logs**:
  - The application includes logging for debugging. Check `uvicorn` output for `INFO` and `ERROR` messages.

## Project Structure
- `main.py`: FastAPI application with API endpoints.
- `models.py`: SQLAlchemy models for database tables.
- `schemas.py`: Pydantic schemas for request/response validation.
- `database.py`: Database configuration and session management.
- `seed.py`: Script to populate the database with sample data.
- `check_db.py`: Debugging script to inspect database contents.
- `requirements.txt`: Python dependencies.
- `data.db`: SQLite database (generated after seeding).
- `.gitignore`: Ignores `data.db`, `venv/`, and other non-essential files.

## Notes
- The application uses SQLite for simplicity.
- The `POST /trips` endpoint creates new `Transfer` objects to avoid foreign key conflicts with existing transfers.
- Recommended itineraries are pre-seeded for 2–8 nights, accessible via `GET /recommend/{nights}`.
- A one-pager PDF (`one-pager.pdf`) is included in the submission, summarizing the project and challenges faced.

## License
This project is for educational purposes and not licensed for commercial use.

---

**Author**: Roshan Baghwar  
**Contact**: roshan.br800@gmail.com 
**Submission Date**: April 29, 2025