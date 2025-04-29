# Travel Itinerary System

Backend system for managing travel itineraries, built for the SDE Intern Assignment. Features a SQLAlchemy-based database, FastAPI RESTful APIs, and an MCP server for recommending itineraries for Phuket and Krabi, Thailand.

## Prerequisites

* Python 3.8+
* Git
* SQLite (included with Python)

## Setup Instructions

1. **Clone the Repository**:

```bash
git clone https://github.com/your-username/travel-itinerary-system.git
cd travel-itinerary-system
```

2. **Set Up Virtual Environment**:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**:

```bash
pip install -r requirements.txt
```

4. **Initialize Database**:
   * Run the seeding script to create and populate the SQLite database:

```bash
python seed.py
```

## Running the Application

1. **Start the FastAPI Server**:

```bash
uvicorn main:app --reload
```

   * The API will be available at `http://localhost:8000`.
   * Access API documentation at `http://localhost:8000/docs`.

2. **Test API Endpoints**:
   * Use tools like Postman or curl to interact with the API.
   * Example requests are provided below.

## API Endpoints

* **POST /trips**: Create a new trip itinerary.
   * Example Request:

```json
{
  "name": "Phuket Getaway",
  "start_date": "2025-05-01",
  "nights": 3,
  "days": [
    {
      "date": "2025-05-01",
      "hotel_id": 1,
      "transfer_ids": [1],
      "activity_ids": [1]
    }
  ]
}
```

* **GET /trips**: List all trip itineraries.
* **GET /trips/{trip_id}**: View a specific trip itinerary.
* **GET /recommend/{nights}**: Get a recommended itinerary for the given number of nights (2-8).

## Project Structure

* `models.py`: SQLAlchemy models for database schema.
* `main.py`: FastAPI application with API endpoints.
* `seed.py`: Script to seed the database with Phuket/Krabi data.
* `database.py`: Database connection and session setup.
* `schemas.py`: Pydantic schemas for API input/output validation.
* `data.db`: SQLite database file.

## Notes

* The database is seeded with realistic data for Phuket and Krabi, including hotels, activities, transfers, and recommended itineraries (2-8 nights).
* The MCP server is implemented as an API endpoint (`/recommend/{nights}`) for simplicity.
* Assumptions and key decisions are documented in the one-pager (submitted separately).