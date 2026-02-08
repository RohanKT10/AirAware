from fastapi import HTTPException
from services.http_client import get_with_retry
from core.config import GEOCODING_URL


async def get_location_from_city(city: str) -> dict:
    """
    Returns geographic coordinates of a city name using the Open-Meteo Geocoding API
    """
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = await get_with_retry(GEOCODING_URL, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="City geocoding failed")

    data = response.json()

    if "results" not in data or not data["results"]:
        raise HTTPException(status_code=404, detail="City not found")

    result = data["results"][0]

    return {
        "city": result["name"],
        "country": result.get("country"),
        "lat": result["latitude"],
        "lon": result["longitude"],
    }