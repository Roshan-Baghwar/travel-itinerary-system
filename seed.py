from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Trip, Day, Hotel, Transfer, Activity, RecommendedItinerary
from datetime import datetime, timedelta

def seed_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Clear existing data
        db.query(Trip).delete()
        db.query(Day).delete()
        db.query(Hotel).delete()
        db.query(Transfer).delete()
        db.query(Activity).delete()
        db.query(RecommendedItinerary).delete()
        
        # Seed Hotels
        hotels = [
            Hotel(name="Hilton Phuket Arcadia", location="Karon Beach"),
            Hotel(name="Centara Grand Krabi", location="Ao Nang"),
            Hotel(name="Marriott Phuket", location="Patong Beach"),
            Hotel(name="Rayaburi Resort", location="Railay Beach")
        ]
        db.add_all(hotels)
        
        # Seed Activities
        activities = [
            Activity(name="Phi Phi Island Tour", location="Phuket"),
            Activity(name="James Bond Island Tour", location="Phuket"),
            Activity(name="Krabi 4-Island Tour", location="Krabi"),
            Activity(name="Snorkeling at Coral Island", location="Phuket")
        ]
        db.add_all(activities)
        
        # Seed Transfers
        transfers = [
            Transfer(description="Phuket Airport to Karon Beach"),
            Transfer(description="Phuket Pier to Hotel"),
            Transfer(description="Krabi Airport to Ao Nang"),
            Transfer(description="Hotel to Railay Beach")
        ]
        db.add_all(transfers)
        db.commit()
        
        # Seed Recommended Itineraries
        itinerary_3_night = RecommendedItinerary(name="Phuket Explorer", nights=3)
        db.add(itinerary_3_night)
        db.commit()
        
        # Seed Days for Recommended Itinerary
        start_date = datetime(2025, 5, 1)
        days = [
            Day(date=start_date + timedelta(days=i), hotel_id=hotels[i % len(hotels)].id)
            for i in range(3)
        ]
        db.add_all(days)
        db.commit()
        
        # Link Days to Itinerary and add Transfers/Activities
        for i, day in enumerate(days):
            day.transfers.append(transfers[i % len(transfers)])
            day.activities.append(activities[i % len(activities)])
            itinerary_3_night.days.append(day)
        db.commit()
        
        print("Database seeded successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()