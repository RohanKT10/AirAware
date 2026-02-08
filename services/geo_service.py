from fastapi import HTTPException
from services.http_client import get_with_retry
from cachetools import TTLCache
from core.logging import logger
from core.config import IPWHO_URL,CACHE_TTL_SECONDS

geo_cache = TTLCache(maxsize=1000, ttl=CACHE_TTL_SECONDS)  # 15 minutes ttl for caching

async def get_location_from_ip(ip: str) -> dict:
    """
    Converts the IP address to geographic location using ipwho.is
    """
     #Cache check
    if ip in geo_cache:
        logger.info(f"[GEO CACHE HIT] {ip}")
        return geo_cache[ip]

    logger.info(f"[GEO CACHE MISS] {ip}")

    # External API call 
    response = await get_with_retry(f"{IPWHO_URL}{ip}")
 
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Geolocation service failed")

    data = response.json()

    # To check if ipwho.is returns success=false on error
    if not data.get("success", False):
        raise HTTPException(status_code=400, detail="Invalid IP address")

    location = {
        "city": data["city"],
        "region": data["region"],
        "country": data["country"],
        "lat": data["latitude"],
        "lon": data["longitude"],
    }

    #Store data in cache
    geo_cache[ip] = location
    return location