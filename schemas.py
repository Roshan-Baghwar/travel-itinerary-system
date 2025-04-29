from pydantic import BaseModel
from typing import List
from datetime import date

class DayCreate(BaseModel):
    date: date
    hotel_id: int
    transfer_ids: List[int]
    activity_ids: List[int]

class TripCreate(BaseModel):
    name: str
    start_date: date
    nights: int
    days: List[DayCreate]

class DayResponse(BaseModel):
    date: date
    hotel_id: int
    transfer_ids: List[int]
    activity_ids: List[int]

class TripResponse(BaseModel):
    id: int
    name: str
    start_date: date
    nights: int
    days: List[DayResponse]

    class Config:
        orm_mode = True