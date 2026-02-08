# AirAware: Location-based AQI Service

**AirAware** is a FastAPI backend that determines a user's location using the IP address and retrieves real-time Air Quality Index (AQI) data. It orchestrates multiple external APIs to provide a seamless "location-aware" experience.

---

## Features

* **Auto-Geolocation:** Automatically detects client IP and resolves it to a physical location.
* **Real-time AQI:** Fetches live US EPA standard Air Quality Index data.
* **City Search:** Endpoint to search for AQI by city name.
* **Resilience:** Implements retry logic, timeouts, and rate limiting.
* **Performance:** In-memory caching to minimize external API calls.

---

##  Project Structure

The project structure for AirAware:

```text
AirAware/
├── core/
│   ├── config.py          # Environment configuration
│   ├── logging.py         # Structured logging setup
│   └── rate_limiter.py    # Sliding window rate limiter
├── models/
│   └── schemas.py         # Pydantic data models
├── routers/
│   ├── aqi.py             # AQI and City endpoints
│   └── health.py          # Health check endpoint
├── services/
│   ├── aqi_service.py     # Open-Meteo integration
│   ├── geo_service.py     # IP Geolocation logic
│   ├── city_geo_service.py# City Geocoding logic
│   ├── ip_service.py      # IP extraction 
│   └── http_client.py     # Async HTTP client with Retries
├── main.py                # Application entry point
├── .env                   # Environment variables
└── requirements.txt       # Project dependencies
 ```
---

## Design Choices
**1. Used external APIs: ipwho.is & Open-Meteo**

Selected ipwho.is for geolocation and Open-Meteo for air quality data because:
* No API Keys Required: Both services are open and free for use, which simplifies deployment.
* Ease of Integration: They provide clean, lightweight JSON responses that map easily to Pydantic schemas.

**2. Caching Strategy (TTL)**

Used In-Memory Caching using cachetools to optimize performance and respect external API rate limits. Time-To-Live(TTL) is configured to 15 minutes (900 seconds). Since air quality data and city geolocation do not change second-by-second, frequent fetching is inefficient.

**3. Rate Limiting**

To prevent API abuse and ensure fair usage, implemented a custom Sliding Window Rate Limiter. It tracks the number of requests per IP address within a rolling 60-second window.Limit is set to 60 requests per minute by default.

**4. Data Validation**
Used Pydantic for strict data validation. It ensures that all incoming data (from external APIs) and outgoing responses strictly match our defined schemas (AQIResponseSchema), preventing any runtime type errors.


## Live Demo
You can test the live API here:  

🔗 **[https://airaware-g729.onrender.com/aqi](https://airaware-g729.onrender.com/aqi)**

Made an Interactive UI using React to display information from the api in a user freindly manner. Deployed using vercel

🔗 **[https://airware-ui-gido.vercel.app](https://airware-ui-gido.vercel.app/)**  *(Source Code: [airaware-ui](https://github.com/RohanKT10/airware-ui))*


*(Note: The free tier of Render may take 50 seconds or more to wake up on the first request. Please be patient!)*

---

## Setup & Installation

Follow these steps to run the application locally.

### 1. Clone the Repository
```bash
git clone https://github.com/RohanKT10/AirAware.git
cd AirAware
 ```

### 2. Create a Virtual Environment
```bash
python -m venv venv   #or python3 -m venv venv for Mac/Linux
venv\Scripts\activate  #or source venv/bin/activate for Mac/Linux
 ```
### 3. Install Dependencies
```bash
pip install -r requirements.txt
 ```
### 4. Configure Environment Variables
Create a file named .env in the root directory and paste the following configuration.
Note: No API keys are required for these services.
```bash
# Environment
ENV=production
# External APIs
OPEN_METEO_AQI_URL=https://air-quality-api.open-meteo.com/v1/air-quality
IPWHO_URL=https://ipwho.is/
GEOCODING_URL=https://geocoding-api.open-meteo.com/v1/search
# Timeouts
HTTP_TIMEOUT=5
# Caching
CACHE_TTL_SECONDS=900
# Rate limiting
RATE_LIMIT=60
WINDOW_SECONDS=60
 ```
### 5. Run the Server
Start the application using Uvicorn:
```bash
uvicorn main:app --reload
 ```
---

## Sample Response

### (`GET /aqi`) returns a structured JSON response
```json
{
  "ip": "103.25.x.x",
  "location": {
    "city": "Kolkata",
    "region": "West Bengal",
    "country": "India",
    "lat": 22.57,
    "lon": 88.36
  },
  "aqi": {
    "value": 152,
    "category": "Unhealthy"
  },
  "source": "open-meteo",
  "timestamp": "2026-02-07T12:47:xx"
}
 ```

### (`GET /aqi/by-city?name=CityName`) to search aqi by City Name
```json
{
  "location": {
    "city": "Calcutta",
    "country": "India",
    "lat": 22.57,
    "lon": 88.36
  },
  "aqi": {
    "value": 152,
    "category": "Unhealthy"
  },
  "source": "open-meteo",
  "timestamp": "2026-02-07T12:47:xx"
}
 ```
