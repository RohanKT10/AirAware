from fastapi import APIRouter,Request,Depends
from services.ip_service import get_client_ip
from services.geo_service import get_location_from_ip
from services.aqi_service import get_aqi
from services.city_geo_service import get_location_from_city
from models.schemas import AQIResponseSchema
from datetime import datetime, timezone
from core.rate_limiter import rate_limiter


router = APIRouter()

@router.get("/aqi", dependencies=[Depends(rate_limiter)],response_model=AQIResponseSchema)
async def get_aqi_for_current_location(request: Request):
    """
    Retrieves the Air Quality Index (AQI) for the client's current location
    """
    #Detect client IP
    ip = await get_client_ip(request)

    #Resolve IP to location
    location = await get_location_from_ip(ip)

    lat = location["lat"]
    lon = location["lon"]

    #Fetch AQI using coordinates
    aqi = await get_aqi(lat, lon)

    #Return final response
    return {
        "ip": ip,
        "location": {
            "city": location["city"],
            "region": location["region"],
            "country": location["country"],
            "lat": lat,
            "lon": lon,
        },
        "aqi": aqi,
        "source": "open-meteo",
        "timestamp": datetime.now(timezone.utc)
    }

@router.get("/aqi/by-city", dependencies=[Depends(rate_limiter)],response_model=AQIResponseSchema,response_model_exclude_none=True)
async def get_aqi_by_city(name: str):
    """
    Retrieves the Air Quality Index (AQI) for a specific city
    """

    #City to coordinates
    location = await get_location_from_city(name)

    #Coordinates to AQI
    aqi = await get_aqi(location["lat"], location["lon"])

    #Response
    return {
        "location": {
            "city": location["city"],
            #"region": location["region"],
            "country": location["country"],
            "lat": location["lat"],
            "lon": location["lon"],
        },
        "aqi": aqi,
        "source": "open-meteo",
        "timestamp": datetime.now(timezone.utc)
    }