from dotenv import load_dotenv
load_dotenv()  # Load environment variables

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.aqi import router as aqi_router
from routers.health import router as health_router
import os

ENV = os.getenv("ENV", "production")

#Docs hidden in production
app = FastAPI(
    title="AirAware",
    docs_url="/docs" if ENV == "development" else None,
    redoc_url="/redoc" if ENV == "development" else None,
    openapi_url="/openapi.json" if ENV == "development" else None,
)

#Configure CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Register API routes
app.include_router(aqi_router)
app.include_router(health_router)
