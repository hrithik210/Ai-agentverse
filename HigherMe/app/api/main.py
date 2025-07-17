from fastapi import FastAPI
from app.scheduler.scheduler import start
from requests import Request
from app.db.database import get_db_session
from app.agents.mood_agent import log_mood
import json


app = FastAPI(
    title="HigherMe API",
    description="API for HigherMe application",
)


@app.post("/log-mood")
async def log_mood(request  : Request):
    
    db = get_db_session()
    
    try:
        data = await request.json()
        mood_text = data.get("mood_text" , "")
        
        print(f"mood text from req: {mood_text}")
        
        log_mood(mood_text)
        print("Mood logged successfully")
        return {"message": "Mood logged successfully"}
    except Exception as e:
        print(f"Error logging mood: {e}")
        return {"error": "Failed to log mood"}


@app.post("/log-meals")
async def log_meals(request: Request):
    db = get_db_session()
    
    try:
        data = await request.json()
        meal = data.get("meal" , "")
        print(f"meal from request  : {meal}")
        log_meals(meal)
        print("Meals logged successfully")
        return json.response({"message": "Meals logged successfully"})
    except Exception as e:
        print(f"Error logging meals: {e}")
        return json.response({"error" : "Failed to log meals"})

@app.on_event("startup")
async def startup_event():
    print("🚀 HigherMe API is starting up...")
    start()
    