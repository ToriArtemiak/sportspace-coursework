
from fastapi import FastAPI

app = FastAPI(
    title="SportSpace API",
    description="Online sports facilities booking system",
    version="0.1.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SportSpace!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
