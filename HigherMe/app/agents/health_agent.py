from app.db import crud
from app.tools.xp_calculator import calculateXp
from datetime import datetime
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from app.db.database import get_db_session
from app.db.models import HealthLog, XPEvent

load_dotenv()

#initializing llm
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
)

def score_meal_sentiment(meal_text: str) -> float:
    prompt = f"""
      Rate the healthiness of this meal on a scale from -1 to 1. 
      Only return a number, no explanation.

      Meal: {meal_text}
      """
    try:
        result = llm.invoke(prompt)
        return float(result.content.strip())
    except Exception as e:
        print(f"Error scoring meal sentiment: {e}")
        return 0.0 

def log_health_activity(meals: str, sleep_hours: float, water_liters: float, exercise_minutes: int):
    """
    Log health activity without calculating XP.
    XP will be calculated by the scheduler at the end of the day.
    """
    db_session = get_db_session()
    try:
        # Store health data
        health_log = crud.create_health_log(
            db=db_session,
            meals=meals,
            sleep_hours=sleep_hours,
            water_intake_liter=water_liters,
            exercise_minutes=exercise_minutes
        )
        print("✅ Health activity logged successfully")
        print("📊 Health XP will be calculated at the end of the day")
        return health_log
    except Exception as e:
        print(f"❌ Error logging health activity: {e}")
    finally:
        db_session.close()

def run_health_agent():
    """
    Calculate XP for all unprocessed health logs.
    This function is called by the scheduler.
    """
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if XP has already been awarded for health today
        xp_awarded = db_session.query(XPEvent).filter(
            XPEvent.timestamp >= today,
            XPEvent.xp_type == "health"
        ).first()
        
        if xp_awarded:
            print(f"⚠️ Health XP already awarded today ({xp_awarded.amount} XP). Skipping.")
            return
        
        # Get unprocessed health logs from today
        health_logs = db_session.query(HealthLog).filter(
            HealthLog.date >= today,
            HealthLog.processed == False
        ).order_by(HealthLog.date).all()
        
        if not health_logs:
            print("ℹ️ No unprocessed health logs found for today. No XP awarded.")
            return
        
        total_xp = 0
        for log in health_logs:
            # Score meals for each log
            meal_score = score_meal_sentiment(log.meals)
            
            # Calculate XP for each log
            metrics = {
                "sleep_hours": log.sleep_hours,
                "water_intake_liters": log.water_intake_liter,
                "exercise_minutes": log.exercise_minutes,
                "meal_score": meal_score,
                "meals": log.meals
            }
            
            xp_result = calculateXp(event_type="health", metrics=metrics)
            total_xp += xp_result["xp"]
            
            # Mark log as processed
            log.processed = True
            log.processed_at = datetime.now()
        
        # Award total XP for the day
        crud.award_daily_xp("health", total_xp)
        db_session.commit()
        
        print(f"🧠 Daily Health XP Awarded: +{total_xp} XP")
        
    except Exception as e:
        print(f"❌ Error calculating health XP: {e}")
        db_session.rollback()
    finally:
        db_session.close()
