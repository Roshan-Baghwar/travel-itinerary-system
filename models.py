from sqlalchemy import Column, Integer, String, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from database import Base

# Many-to-many relationship table for Day and Activity
day_activity = Table(
    'day_activity', Base.metadata,
    Column('day_id', Integer, ForeignKey('day.id'), primary_key=True),
    Column('activity_id', Integer, ForeignKey('activity.id'), primary_key=True)
)

# Many-to-many relationship table for RecommendedItinerary and Day
recommended_itinerary_day = Table(
    'recommended_itinerary_day', Base.metadata,
    Column('itinerary_id', Integer, ForeignKey('recommended_itinerary.id'), primary_key=True),
    Column('day_id', Integer, ForeignKey('day.id'), primary_key=True)
)

class Trip(Base):
    __tablename__ = 'trip'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, index=True)
    start_date = Column(Date, nullable=False)
    nights = Column(Integer, nullable=False)
    days = relationship("Day", back_populates="trip", cascade="all, delete-orphan")

class Day(Base):
    __tablename__ = 'day'
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey('trip.id'), nullable=True)  # Changed to nullable=True
    date = Column(Date, nullable=False)
    trip = relationship("Trip", back_populates="days")
    hotel_id = Column(Integer, ForeignKey('hotel.id'))
    hotel = relationship("Hotel")
    transfers = relationship("Transfer", cascade="all, delete-orphan")
    activities = relationship("Activity", secondary=day_activity)

class Hotel(Base):
    __tablename__ = 'hotel'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

class Transfer(Base):
    __tablename__ = 'transfer'
    id = Column(Integer, primary_key=True)
    day_id = Column(Integer, ForeignKey('day.id'), nullable=False)
    description = Column(String, nullable=False)

class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)

class RecommendedItinerary(Base):
    __tablename__ = 'recommended_itinerary'
    id = Column(Integer, primary_key=True)
    nights = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    days = relationship("Day", secondary=recommended_itinerary_day)