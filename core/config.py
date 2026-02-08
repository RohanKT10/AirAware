import os

ENV = os.getenv("ENV", "production")

OPEN_METEO_AQI_URL = os.getenv("OPEN_METEO_AQI_URL")
IPWHO_URL = os.getenv("IPWHO_URL")
GEOCODING_URL=os.getenv("GEOCODING_URL")

HTTP_TIMEOUT = int(os.getenv("HTTP_TIMEOUT", 5))
CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 900))

RATE_LIMIT = int(os.getenv("RATE_LIMIT", 60))
WINDOW_SECONDS = int(os.getenv("WINDOW_SECONDS", 60))