from fastapi import Request
import httpx
from core.config import HTTP_TIMEOUT


async def get_client_ip(request: Request) -> str:
    """
    Extracts the client IP from request headers.
    Falls back to public IP address if needed
    """
   
    #For proxy address
    x_forwarded_for = request.headers.get("x-forwarded-for")
    if x_forwarded_for:
        # return 1st IP if there are multiple IP
        return x_forwarded_for.split(",")[0].strip()
    
    #Direct connection
    if request.client:
        ip = request.client.host
        if ip not in ("127.0.0.1", "::1"):
            return ip

    #Public ip address using ipfy  
    async with httpx.AsyncClient(timeout=HTTP_TIMEOUT) as client:
        response = await client.get("https://api.ipify.org")
        response.raise_for_status()
        return response.text.strip()