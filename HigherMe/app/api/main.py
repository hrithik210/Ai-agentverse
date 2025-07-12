from fastapi import FastAPI
from app.scheduler.scheduler import start


app = FastAPI(
    title="HigherMe API",
    description="API for HigherMe application",
)


@app.on_event("startup")
async def startup_event():
    print("🚀 HigherMe API is starting up...")
    start()
    