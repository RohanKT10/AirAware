from fastapi import HTTPException
from services.http_client import get_with_retry
from cachetools import TTLCache
from core.logging import logger
from core.config import OPEN_METEO_AQI_URL, CACHE_TTL_SECONDS

aqi_cache = TTLCache(maxsize=1000, ttl=CACHE_TTL_SECONDS)


def map_aqi_category(aqi: int) -> str:
    """
    This classification follows the official United States Environmental Protection 
    Agency (EPA) Air Quality Index (AQI) standards as defined by AirNow.gov
    """
    if aqi <= 50:
        return "Good"
    elif aqi <= 100:
        return "Moderate"
    elif aqi <= 150:
        return "Unhealthy for Sensitive Groups"
    elif aqi <= 200:
        return "Unhealthy"
    elif aqi <= 300:
        return "Very Unhealthy"
    else:
        return "Hazardous"


async def get_aqi(lat: float, lon: float) -> dict:
    """
    To fetch AQI data from Open-Meteo using coordinates
    """
    cache_key = f"{lat}:{lon}"

    #Cache check
    if cache_key in aqi_cache:
        logger.info(f"[AQI CACHE HIT] {cache_key}")
        return aqi_cache[cache_key]

    logger.info(f"[AQI CACHE MISS] {cache_key}")

    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "us_aqi",
    }

    response = await get_with_retry(OPEN_METEO_AQI_URL, params)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="AQI service unavailable")

    data = response.json()

    try:
        aqi_value = data["current"]["us_aqi"]
    except KeyError:
        raise HTTPException(status_code=500, detail="Invalid AQI response")

    result = {
        "value": aqi_value,
        "category": map_aqi_category(aqi_value),
    }

    #Store cache data
    aqi_cache[cache_key] = result
    return result
