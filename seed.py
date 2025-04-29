from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from models import Trip, Day, Hotel, Transfer, Activity, RecommendedItinerary
from datetime import datetime, timedelta
import traceback

def seed_db():
    # Create tables
    try:
        Base.metadata.drop_all(bind=engine)  # Clear existing tables
        Base.metadata.create_all(bind=engine)
    except Exception as e:
        print(f"Error creating tables: {e}")
        return
    
    db = SessionLocal()
    try:
        # Clear existing data (redundant but ensures clean slate)
        db.query(Trip).delete()
        db.query(Day).delete()
        db.query(Hotel).delete()
        db.query(Transfer).delete()
        db.query(Activity).delete()
        db.query(RecommendedItinerary).delete()
        db.commit()
        
        # Seed Hotels
        hotels = [
            Hotel(name="Hilton Phuket Arcadia", location="Karon Beach"),
            Hotel(name="Centara Grand Krabi", location="Ao Nang"),
            Hotel(name="Marriott Phuket", location="Patong Beach"),
            Hotel(name="Rayaburi Resort", location="Railay Beach"),
            Hotel(name="Amari Phuket", location="Patong Beach")
        ]
        db.add_all(hotels)
        db.commit()
        print(f"Seeded {len(hotels)} hotels")
        
        # Seed Activities
        activities = [
            Activity(name="Phi Phi Island Tour", location="Phuket"),
            Activity(name="James Bond Island Tour", location="Phuket"),
            Activity(name="Krabi 4-Island Tour", location="Krabi"),
            Activity(name="Snorkeling at Coral Island", location="Phuket"),
            Activity(name="Emerald Pool Trek", location="Krabi")
        ]
        db.add_all(activities)
        db.commit()
        print(f"Seeded {len(activities)} activities")
        
        # Seed Recommended Itineraries (2-8 nights)
        itineraries = [
            RecommendedItinerary(name=f"{n}-Night Phuket & Krabi Adventure", nights=n)
            for n in range(2, 9)
        ]
        db.add_all(itineraries)
        db.commit()
        print(f"Seeded {len(itineraries)} itineraries")
        
        # Seed Days and Transfers for each Itinerary
        start_date = datetime(2025, 5, 1)
        transfer_descriptions = [
            "Phuket Airport to Karon Beach",
            "Phuket Pier to Hotel",
            "Krabi Airport to Ao Nang",
            "Hotel to Railay Beach",
            "Patong to Karon Beach"
        ]
        
        for itinerary in itineraries:
            days = [
                Day(date=start_date + timedelta(days=i), hotel_id=hotels[i % len(hotels)].id)
                for i in range(itinerary.nights)
            ]
            db.add_all(days)
            db.commit()
            print(f"Seeded {len(days)} days for {itinerary.name}")
            
            # Create Transfers and link to Days
            for i, day in enumerate(days):
                # Create a new Transfer for this Day
                transfer = Transfer(
                    day_id=day.id,
                    description=transfer_descriptions[i % len(transfer_descriptions)]
                )
                db.add(transfer)
                day.transfers.append(transfer)
                day.activities.append(activities[i % len(activities)])
                itinerary.days.append(day)
            db.commit()
            print(f"Linked days, transfers, and activities for {itinerary.name}")
        
        print("Database seeded successfully!")
    except Exception as e:
        print(f"Error seeding database: {e}")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()