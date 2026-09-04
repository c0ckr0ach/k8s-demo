import os
import redis
from fastapi import FastAPI, Response, status

app = FastAPI(title= "Gitops microservice API")

ENVIRONMENT = os.getenv("APP_ENV", "local")
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        decode_responses=True,
        socket_connect_timeout=1
    )

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint to verify the service is functioning correctly.
    Returns a 200 OK response if the service is healthy.
    """
    return {"status": "healthy"}

def get_status():
    """Service status and Redis connectivity check."""
    redis_connected = False
    visits = 0

    if r:
        try:
            visits = r.incr("page_visits")
            redis_connected = True
        except redis.ConnectionError:
            redis_connected = False

    return {
        "service": "backend-api",
        "framework": "FastAPI",
        "redis_connected": redis_connected,
        "visit_count": visits if redis_connected else "redis_offline"
    }