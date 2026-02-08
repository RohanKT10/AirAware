import httpx
import asyncio
from fastapi import HTTPException
from core.logging import logger
from core.config import HTTP_TIMEOUT

async def get_with_retry(url: str, params: dict | None = None, retries: int = 3):
    """
    Executes an asynchronous HTTP GET request with automatic retries
    """
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
                return await client.get(url, params=params)

        except httpx.RequestError as e:
            logger.warning(f"HTTP attempt {attempt}/{retries} failed: {e}")

            if attempt == retries - 1:
                logger.error("All retry attempts failed")

            await asyncio.sleep(0.5)  # cool down time 

    raise HTTPException(status_code=504, detail="External service unavailable after retries")