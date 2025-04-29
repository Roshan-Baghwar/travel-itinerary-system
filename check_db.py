from database import SessionLocal
from models import RecommendedItinerary

db = SessionLocal()
try:
    itineraries = db.query(RecommendedItinerary).all()
    for it in itineraries:
        print(f"ID: {it.id}, Name: {it.name}, Nights: {it.nights}, Days: {len(it.days)}")
    if not itineraries:
        print("No recommended itineraries found in the database.")
finally:
    db.close()