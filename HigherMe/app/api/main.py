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
from app.auth.auth import get_password_hash , verify_password, create_access_token
from fastapi.middleware.cors import CORSMiddleware

# Configure CORS
app = FastAPI(
    title="HigherMe API",
    description="API for HigherMe application",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()


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


@app.get("/api/v1/daily-report")
async def get_daily_report(db : Session = Depends(get_db) , current_user  : User = Depends(get_current_user)):
    try:
        report = build_daily_report(db , current_user.id)
        return {"report" : report}
    except Exception as e:
        print(f"error occured : {e}")
        raise HTTPException(status_code=500 , detail= str(e))
    
@app.get("/api/v1/stats")
def get_user_stats(db : Session = Depends(get_db) , current_user : User = Depends(get_current_user)):
    try:
        level = db.query(Level).filter(Level.user_id == current_user.id).first()
        
        today = datetime.now().date()
        today_xp = db.query(XPEvent).filter(
            XPEvent.timestamp >= today,
            XPEvent.user_id == current_user.id
            ).all()
        return {
            "current_level" : level.current_level if level else 1,
            "total_xp" : level.total_xp if level else 0,
            "todays_xp" : sum(xp.amount for xp in today_xp),
            "xp_breakdown" : {xp.xp_type : xp.amount for xp in today_xp}
        }
    except Exception as e:
        print(f"error in getting stats : {e}")
        raise HTTPException(status_code=500 , detail = str(e))


@app.post("/api/v1/auth/register")
async def register(req : Request):
    try:
        data = await req.json()
        username = data.get("username").strip().lower()
        email = data.get("email").strip().lower()
        password = data.get("password")
        
        if not username or len(username) < 3:
            raise HTTPException(status_code=400 , detail="username too small")
        
        if not email or "@" not in email :
            raise HTTPException(status_code=400  , detail= "invalid email lil bro")
        
        if not password or len(password) < 6:
            raise HTTPException(status_code=400 , detail="password must be atleast 6 characters long")

        db = get_db_session()
        
        try:
            #checking for existing user
            existing_user = db.query(User).filter(
                (User.username == username) | (User.email == email)
            ).first()
            
            if existing_user:
                if existing_user.email:
                    raise HTTPException(status_code=400 , detail="email already in use")
                else:
                    raise HTTPException(status_code=400 , detail="username taken")
            
            #hashing password
            hashed_password = get_password_hash(password)
            
            new_user = User(
                username=username,
                email=email,
                hashed_password = hashed_password,
                created_at = datetime.now(),
                is_active = True
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Create initial level record for the new user
            from app.db.models import Level
            initial_level = Level(
                user_id=new_user.id,
                current_level=1,
                total_xp=0,
                last_updated=datetime.now()
            )
            db.add(initial_level)
            db.commit()
            
            #creating access token
            token = create_access_token(data={"sub" : new_user.username})
            
            return {
                "message" : "user registered successfully",
                "access_token" : token,
                "token_type" : "bearer",
                "user" : {
                    "id" : new_user.id,
                    "username" : new_user.username,
                    "email" : new_user.email
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"registration error : {e}")
            db.rollback()
            raise HTTPException(status_code=500 ,  detail="error registring user")
        finally:
            db.close()
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration request error: {e}")
        raise HTTPException(status_code=400, detail="Invalid request data")


@app.post("/api/v1/auth/login")
async def login(req : Request):
    try:
        data = await req.json()
        login_identifier = data.get("email").strip().lower()
        password = data.get("password")
        
        if not login_identifier:
            raise HTTPException(status_code=400 , detail= "email missing")
        if not password:
            raise HTTPException(status_code=400 , detail= "password cant be empty")
    

        db = get_db_session()
        
        try:
            user = db.query(User).filter(
                (User.email == login_identifier) | (User.username == login_identifier)
            ).first()
            
            if not user:
                raise HTTPException(status_code=401 , detail="invalid credentials")
            
            if not user.is_active:
                raise HTTPException(status_code=401 , detail="account deactivated")
            
            if not verify_password(password , user.hashed_password):
                raise HTTPException(status_code=401 , detail="invalid password")

            token = create_access_token(data= {"sub" : user.username})
            
            return {
                "message" : "login success",
                "access_token" : token,
                "token_type" : "bearer",
                "user": {
                    "id" : user.id,
                    "username" : user.username,
                    "email" : user.email
                }
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"error while loggin in : {e}")
            raise HTTPException(status_code=500 , detail="something went wrong")
        finally:
            db.close()
    
    except HTTPException:
        raise
    except Exception as e:
        print("login req error : {e}")
        raise HTTPException(status_code=400, detail="Invalid request data")
 
 
@app.get("/api/v1/auth/me")
async def get_current_user_info(current_user : User = Depends(get_current_user)):
    return {
        "user" : {
            "id" : current_user.id,
            "username" : current_user.username,
            "email"  : current_user.email,
            "created_at" : current_user.created_at,
            "is_active" : current_user.is_active
        }
    }

        
@app.on_event("startup")
async def startup_event():
    print("🚀 HigherMe API is starting up...")
    start()
    print("Scheduler started for daily tasks.")