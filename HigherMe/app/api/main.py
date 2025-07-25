from fastapi import FastAPI, Request , HTTPException , Depends
from app.scheduler.scheduler import start
from app.db.database import get_db_session
from app.agents.mood_agent import log_mood
from app.agents.code_agent import log_code_activity
from app.agents.health_agent import log_meal , log_exercise , log_sleep , log_water_intake
from app.agents.daily_report_agent import build_daily_report
from sqlalchemy.orm import Session
from app.db.models import Level , XPEvent , CodeLog
from datetime import datetime
from app.auth.auth import get_current_user
from app.db.models import User



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
async def create_mood_log(request  : Request, current_user : User = Depends(get_current_user)):
    
    
    try:
        data = await request.json()
        mood_text = data.get("mood_text" , "")
        
        print(f"mood text from req: {mood_text}")
        
        log_mood(mood_text , current_user.id)
        print("Mood logged successfully")
        return {"message": "Mood logged successfully",}
    except Exception as e:
        print(f"Error logging mood: {e}")
        raise HTTPException(status_code=500 , detail=str(e))


@app.post("/api/v1/health/meal")
async def create_meal_log(request: Request, current_user : User = Depends(get_current_user)):
    try:
        data = await request.json()
        meal = data.get("meal" , "")
        print(f"meal from request  : {meal}")
        log_meal(meal , current_user.id)
        print("Meal logged successfully")
        return {"message": "Meals logged successfully"}
    except Exception as e:
        print(f"Error logging meals: {e}")
        raise HTTPException(status_code=500 , detail=str(e))



@app.post("/api/v1/health/exercise")
async def create_exercise_log(req  : Request, current_user : User = Depends(get_current_user)):
    
    try:
       data = await req.json()
       exercise_minutes = data.get("exercise_minutes" , 0)
       print(f"excercise minutes from request :  {exercise_minutes}")
       
       log_exercise(exercise_minutes , current_user.id)
       print("Exercise logged successfully")
       response = {"message": "Exercise logged successfully"}
       return response
    except Exception as e:
        print(f"Error logging exercise: {e}")
        raise HTTPException(status_code=500 , detail=str(e))

@app.post("/api/v1/health/sleep")
async def create_sleep_log(req : Request, current_user : User = Depends(get_current_user)):
    
    try:
        data = await req.json()
        
        sleep_hours = data.get("sleep_hours" , 0)
        print(f"Sleep hours from request: {sleep_hours}")
        log_sleep(sleep_hours , current_user.id)
        print("sleep logged successfully")
        return {"message": "Sleep logged successfully"}
    
    except Exception as e:
        print(f"Error logging sleep: {e}")
        raise HTTPException(status_code=500 , detail=str(e))

@app.post("/api/v1/health/water")
async def create_water_log(req: Request, current_user : User = Depends(get_current_user)):    
    try:
        data = await req.json()
        water_intake_liter  = data.get("water_intake", 0.0)
        log_water_intake(water_intake_liter , current_user.id)
        print("Water intake logged successfully")
        return {"message": "Water intake logged successfully"}
    except Exception as e:
        print(f"Error logging water intake: {e}")
        raise HTTPException(status_code=500 , detail=str(e))
    

@app.post("/api/v1/create-code-activity")
async def create_code_activity(current_user : User = Depends(get_current_user)):
    try:
        code_activity = log_code_activity(current_user.id)
        
        return {
            "message" : "code logs created",
            "log_id" : code_activity.id
            }
    
    except Exception as e:
        print(f"Error logging code activity: {e}")
        return {"error": "Failed to load code activity"}

@app.get("/api/v1/get-code-activity")
async def get_code_activity(current_user : User = Depends(get_current_user) , db : Session = Depends(get_db)):
    try: 
        today  = datetime.now().date()
        
        #todays's code logs
        code_logs = db.query(CodeLog).filter(
            CodeLog.user_id == current_user.id,
            CodeLog.date >= today
        ).all()
        
        return {
            "code_logs": [
                {
                    "id": log.id,
                    "lines_added": log.lines_added,
                    "lines_removed": log.lines_removed,
                    "total_time_minutes": log.total_time_minutes,
                    "date": log.date.isoformat(),
                    "processed": log.processed
                }
                for log in code_logs
            ],
            "total_logs": len(code_logs)
        }
    
    except Exception as e:
        print(f"error getting code logs: {e}")
        return {"message" : "error getting code logs"}


@app.get("/appi/v1/daily-report")
async def get_daily_report(db : Session = Depends(get_db())):
    try:
        report = build_daily_report(db)
        return {"report" : report}
    except Exception as e:
        print(f"error occured : {e}")
        raise HTTPException(status_code=500 , detail= str(e))
    
@app.get("/api/v1/stats")
def get_user_stats(db : Session = Depends(get_db())):
    try:
        level = db.query(Level).first()
        
        today = datetime.now().date()
        today_xp = db.query(XPEvent).filter(XPEvent.timestamp >= today).all()
        return {
            "current_level" : level.current_level if level else 1,
            "total_xp" : level.total_xp if level else 0,
            "todays_xp" : sum(xp.amount for xp in today_xp),
            "xp_breakdown" : {xp.xp_type : xp.amount for xp in today_xp}
        }
    except Exception as e:
        print(f"error in getting stats : {e}")
        raise HTTPException(status_code=500 , detail = str(e))


      
@app.on_event("startup")
async def startup_event():
    print("🚀 HigherMe API is starting up...")
    start()
    