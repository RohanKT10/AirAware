from pydantic import BaseModel
from datetime import datetime
from typing import Optional

#Schema to represent geographic location details
class LocationSchema(BaseModel):
    city: str
    region: Optional[str] = None 
    country: str
    lat: float
    lon: float

#Schema for Air Quality Index data
class AQISchema(BaseModel):
    value: int
    category: str

#Final response schema
class AQIResponseSchema(BaseModel):
    ip: Optional[str] = None  
    location: LocationSchema
    aqi: AQISchema
    source: str
    timestamp: datetime