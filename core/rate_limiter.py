from fastapi import Request, HTTPException
from cachetools import TTLCache
from core.logging import logger
from core.config import RATE_LIMIT,WINDOW_SECONDS 

rate_limit_cache = TTLCache(maxsize=10_000, ttl=WINDOW_SECONDS)

async def rate_limiter(request: Request):
    """
    Sliding window rate limiting mechanism to prevent API abuse
    """

    if not request.client:
        raise HTTPException(status_code=400, detail="Cannot determine client IP")

    client_ip = request.client.host
    count = rate_limit_cache.get(client_ip, 0)

    if count >= RATE_LIMIT:
        logger.warning(f"Rate limit exceeded for IP {client_ip}")
        raise HTTPException(status_code=429,detail="Too many requests. Please try again later.")

    rate_limit_cache[client_ip] = count + 1
