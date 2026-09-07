import os
import redis
from fastapi import FastAPI, status

app = FastAPI(title= "Gitops microservice API")

ENVIRONMENT = os.getenv("APP_ENV", "local")
REDIS_HOST = os.getenv("REDIS_HOST", "redis-service")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def get_redis_client():
    return redis.Redis(
        host=REDIS_HOST, 
        port=REDIS_PORT, 
        decode_responses=True,
        socket_connect_timeout=2
    )

redis_client = get_redis_client()

@app.get("/healthz", status_code=status.HTTP_200_OK)
def health_check():
    """
    Health check endpoint for kubernetes liveness and readiness probes
    """
    return {"status": "healthy"}
@app.get("/")
@app.get("/api/status")
def get_status():
    """Service status and Redis connectivity check."""
    redis_connected = False
    visits = 0

    try:
        visits = redis_client.incr("page_visits")
        redis_connected = True
    except (redis.ConnectionError, redis.TimeoutError):
        redis_connected = False

    return {
        "service": "backend-api",
        "framework": "FastAPI",
        "redis_connected": redis_connected,
        "visit_count": visits if redis_connected else "redis_offline"
    }