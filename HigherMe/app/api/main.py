from fastapi import FastAPI
from app.scheduler.scheduler import start
from requests import Request
from app.db.database import get_db_session
from app.agents.mood_agent import log_mood
from app.agents.code_agent import log_code_activity
import json


app = FastAPI(
    title="HigherMe API",
    description="API for HigherMe application",
)


@app.post("/log-mood")
async def log_mood(request  : Request):
    
    
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

    
    try:
        data = await request.json()
        meal = data.get("meal" , "")
        print(f"meal from request  : {meal}")
        log_meals(meal)
        print("Meals logged successfully")
        return {"message": "Meals logged successfully"}
    except Exception as e:
        print(f"Error logging meals: {e}")
        response = {"error": "Failed to log meals"}
   
        return json


@app.post("/log-exercise")
async def log_excercise(req  : Request):
    
    try:
       data = await req.json()
       exercise_minutes = data.get("excercise_minutes" , 0)
       print(f"excercise minutes from request :  {exercise_minutes}")
       
       log_excercise(exercise_minutes)
       print("Exercise logged successfully")
       response = {"message": "Exercise logged successfully"}
       return response
    except Exception as e:
        print(f"Error logging exercise: {e}")
        return {"error": "Failed to log exercise"}

@app.post("/log-sleep")
async def log_sleep(req : Request):
    
    try:
        data = await req.json()
        
        sleep_hours = data.get("sleep_hours" , 0)
        print(f"Sleep hours from request: {sleep_hours}")
        log_sleep(sleep_hours)
        print("sleep logged successfully")
        return {"message": "Sleep logged successfully"}
    
    except Exception as e:
        print(f"Error logging sleep: {e}")
        return {"error": "Failed to log sleep"}

@app.post("/log-water-intake")
async def log_water_intake(req: Request):    
    try:
        data = await req.json()
        water_intake_liter  = data.get("water_intake", 0.0)
        log_water_intake(water_intake_liter)
        print("Water intake logged successfully")
        return {"message": "Water intake logged successfully"}
    except Exception as e:
        print(f"Error logging water intake: {e}")
        return {"error": "Failed to log water intake"}
    

@app.get("/code-activity")
async def get_code_activity():
    try:
        code_activity = log_code_activity()
        
        return code_activity
    
    except Exception as e:
        print(f"Error fetching code activity: {e}")
        return {"error": "Failed to fetch code activity"}

@app.on_event("startup")
async def startup_event():
    print("🚀 HigherMe API is starting up...")
    start()
    