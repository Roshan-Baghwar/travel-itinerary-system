from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models import Trip, Day, Hotel, Transfer, Activity, RecommendedItinerary
from schemas import TripCreate, TripResponse, DayCreate, DayResponse
from datetime import datetime

app = FastAPI(title="Travel Itinerary System")

@app.post("/trips", response_model=TripResponse)
def create_trip(trip: TripCreate, db: Session = Depends(get_db)):
    if len(trip.days) != trip.nights:
        raise HTTPException(status_code=400, detail="Number of days must match nights")
    
    for day in trip.days:
        if not db.query(Hotel).filter(Hotel.id == day.hotel_id).first():
            raise HTTPException(status_code=400, detail=f"Invalid hotel_id: {day.hotel_id}")
        for aid in day.activity_ids:
            if not db.query(Activity).filter(Activity.id == aid).first():
                raise HTTPException(status_code=400, detail=f"Invalid activity_id: {aid}")
        for tid in day.transfer_ids:
            if not db.query(Transfer).filter(Transfer.id == tid).first():
                raise HTTPException(status_code=400, detail=f"Invalid transfer_id: {tid}")
    
    db_trip = Trip(name=trip.name, start_date=trip.start_date, nights=trip.nights)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    
    for day_data in trip.days:
        db_day = Day(trip_id=db_trip.id, date=day_data.date, hotel_id=day_data.hotel_id)
        db.add(db_day)
        db.commit()
        db.refresh(db_day)
        # Create new Transfers
        for tid in day_data.transfer_ids:
            transfer = db.query(Transfer).filter(Transfer.id == tid).first()
            new_transfer = Transfer(
                day_id=db_day.id,
                description=transfer.description
            )
            db.add(new_transfer)
        # Link Activities
        for aid in day_data.activity_ids:
            activity = db.query(Activity).filter(Activity.id == aid).first()
            db_day.activities.append(activity)
        db.commit()
    
    # Reload trip with relationships for response
    db_trip = db.query(Trip).options(
        joinedload(Trip.days).joinedload(Day.transfers),
        joinedload(Trip.days).joinedload(Day.activities)
    ).filter(Trip.id == db_trip.id).first()
    
    # Manually construct TripResponse
    trip_response = TripResponse(
        id=db_trip.id,
        name=db_trip.name,
        start_date=db_trip.start_date,
        nights=db_trip.nights,
        days=[
            DayResponse(
                date=day.date,
                hotel_id=day.hotel_id,
                transfer_ids=[t.id for t in day.transfers],
                activity_ids=[a.id for a in day.activities]
            )
            for day in db_trip.days
        ]
    )
    return trip_response

@app.get("/trips", response_model=List[TripResponse])
def get_trips(db: Session = Depends(get_db)):
    trips = db.query(Trip).options(
        joinedload(Trip.days).joinedload(Day.transfers),
        joinedload(Trip.days).joinedload(Day.activities)
    ).all()
    # Manually construct TripResponse list
    trip_responses = [
        TripResponse(
            id=trip.id,
            name=trip.name,
            start_date=trip.start_date,
            nights=trip.nights,
            days=[
                DayResponse(
                    date=day.date,
                    hotel_id=day.hotel_id,
                    transfer_ids=[t.id for t in day.transfers],
                    activity_ids=[a.id for a in day.activities]
                )
                for day in trip.days
            ]
        )
        for trip in trips
    ]
    return trip_responses

@app.get("/trips/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)):
    trip = db.query(Trip).options(
        joinedload(Trip.days).joinedload(Day.transfers),
        joinedload(Trip.days).joinedload(Day.activities)
    ).filter(Trip.id == trip_id).first()
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    
    # Manually construct TripResponse
    trip_response = TripResponse(
        id=trip.id,
        name=trip.name,
        start_date=trip.start_date,
        nights=trip.nights,
        days=[
            DayResponse(
                date=day.date,
                hotel_id=day.hotel_id,
                transfer_ids=[t.id for t in day.transfers],
                activity_ids=[a.id for a in day.activities]
            )
            for day in trip.days
        ]
    )
    return trip_response

@app.get("/recommend/{nights}", response_model=TripResponse)
def recommend_itinerary(nights: int, db: Session = Depends(get_db)):
    if nights < 2 or nights > 8:
        raise HTTPException(status_code=400, detail="Nights must be between 2 and 8")
    
    itinerary = db.query(RecommendedItinerary).options(
        joinedload(RecommendedItinerary.days).joinedload(Day.transfers),
        joinedload(RecommendedItinerary.days).joinedload(Day.activities)
    ).filter(RecommendedItinerary.nights == nights).first()
    if not itinerary:
        print(f"No itinerary found for {nights} nights")  # Debug log
        raise HTTPException(status_code=404, detail="No recommended itinerary found")
    
    trip_response = TripResponse(
        id=itinerary.id,
        name=itinerary.name,
        start_date=itinerary.days[0].date if itinerary.days else datetime(2025, 5, 1).date(),
        nights=itinerary.nights,
        days=[
            DayResponse(
                date=day.date,
                hotel_id=day.hotel_id,
                transfer_ids=[t.id for t in day.transfers],
                activity_ids=[a.id for a in day.activities]
            )
            for day in itinerary.days
        ]
    )
    print(f"Returning itinerary: {itinerary.name} with {len(itinerary.days)} days")  # Debug log
    return trip_response