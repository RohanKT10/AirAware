from fastapi import FastAPI,Request
from dotenv import load_dotenv  

load_dotenv()  #Load environment variables
from services.geo_service import get_location_from_ip
from services.ip_service import get_client_ip
from services.aqi_service import get_aqi

app = FastAPI()

#Test Geolocation
@app.get("/test-geo")
async def test_geo(ip: str):
    return await get_location_from_ip(ip)

#Test IP Detection
@app.get("/test-ip")
async def test_ip(request: Request):
    ip = await get_client_ip(request)
    return {"detected_ip": ip}

#Test AQI Fetching
@app.get("/test-aqi")
async def test_aqi(lat: float, lon: float):
    return await get_aqi(lat, lon)