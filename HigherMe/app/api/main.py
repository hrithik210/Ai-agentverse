from fastapi import FastAPI, Request , HTTPException , Depends
from app.scheduler.scheduler import start
from app.db.database import get_db_session
from app.agents.mood_agent import log_mood
from app.agents.code_agent import log_code_activity
from app.agents.health_agent import log_meal , log_exercise , log_sleep , log_water_intake
from app.agents.daily_report_agent import build_daily_report
from sqlalchemy.orm import Session


def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(
    title="HigherMe API",
    description="API for HigherMe application",
)


@app.post("/api/v1/mood")
async def create_mood_log(request  : Request):
    
    
    try:
        data = await request.json()
        mood_text = data.get("mood_text" , "")
        
        print(f"mood text from req: {mood_text}")
        
        log_mood(mood_text)
        print("Mood logged successfully")
        return {"message": "Mood logged successfully",}
    except Exception as e:
        print(f"Error logging mood: {e}")
        raise HTTPException(status_code=500 , detail=str(e))


@app.post("/api/v1/health/meal")
async def create_meal_log(request: Request):
    try:
        data = await request.json()
        meal = data.get("meal" , "")
        print(f"meal from request  : {meal}")
        log_meal(meal)
        print("Meal logged successfully")
        return {"message": "Meals logged successfully"}
    except Exception as e:
        print(f"Error logging meals: {e}")
        raise HTTPException(status_code=500 , detail=str(e))



@app.post("/log-exercise")
async def create_exercise_log(req  : Request):
    
    try:
       data = await req.json()
       exercise_minutes = data.get("exercise_minutes" , 0)
       print(f"excercise minutes from request :  {exercise_minutes}")
       
       log_exercise(exercise_minutes)
       print("Exercise logged successfully")
       response = {"message": "Exercise logged successfully"}
       return response
    except Exception as e:
        print(f"Error logging exercise: {e}")
        raise HTTPException(status_code=500 , detail=str(e))

@app.post("/api/v1/health/sleep")
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
        raise HTTPException(status_code=500 , detail=str(e))

@app.post("/api/v1/health/water")
async def create_water_log(req: Request):    
    try:
        data = await req.json()
        water_intake_liter  = data.get("water_intake", 0.0)
        log_water_intake(water_intake_liter)
        print("Water intake logged successfully")
        return {"message": "Water intake logged successfully"}
    except Exception as e:
        print(f"Error logging water intake: {e}")
        raise HTTPException(status_code=500 , detail=str(e))
    

@app.get("/api/v1/code-activity")
async def get_code_activity():
    try:
        code_activity = log_code_activity()
        
        return code_activity
    
    except Exception as e:
        print(f"Error fetching code activity: {e}")
        return {"error": "Failed to fetch code activity"}

@app.get("/appi/v1/daily-report")
async def get_daily_report(db : Session = Depends(get_db())):
    try:
        report = build_daily_report(db)
        return {"report" : report}
    except Exception as e:
        print(f"error occured : {e}")
        raise HTTPException(status_code=500 , detail= str(e))
    


@app.on_event("startup")
async def startup_event():
    print("🚀 HigherMe API is starting up...")
    start()
    