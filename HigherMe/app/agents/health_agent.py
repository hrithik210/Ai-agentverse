from db import crud
from tools.xp_calculator import calculateXp
from datetime import datetime, timedelta
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from db.database import get_db_session
from db.models import HealthLog, XPEvent

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

def log_meal(meal_description: str , user_id : int):
    """
    Log a single meal entry and immediately award XP.
    Each meal logged earns XP instantly like a real gaming system.
    """
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if we already have a health log for today to get sleep and exercise
        existing_log = db_session.query(HealthLog).filter(
            HealthLog.user_id == user_id,
            HealthLog.date >= today,
            HealthLog.date < today + timedelta(days=1)
        ).order_by(HealthLog.date.desc()).first()
        
        # Use existing values or defaults
        sleep_hours = existing_log.sleep_hours if existing_log else 0.0
        exercise_minutes = existing_log.exercise_minutes if existing_log else 0
        water_intake = existing_log.water_intake_liter if existing_log else 0.0
        
        # For meals, we either use the existing one and append, or create new
        meals = f"{existing_log.meals}, {meal_description}" if existing_log and existing_log.meals else meal_description
        
        # Store health data (creating new or updating)
        health_log = crud.create_health_log(
            user_id=user_id,
            db=db_session,
            meals=meals,
            sleep_hours=sleep_hours,
            water_intake_liter=water_intake,
            exercise_minutes=exercise_minutes
        )
        
        # Calculate and award XP immediately for this meal
        # Simple meal scoring: assume neutral meal (0) for now, can be enhanced later
        meal_score = 0.0  # Range: -1 (unhealthy) to 1 (very healthy)
        from tools.xp_calculator import calculateXp
        xp_result = calculateXp(event_type="health", metrics={
            "meal_score": meal_score,
            "activity_type": "meal",
            "description": meal_description
        })
        
        # Award XP immediately
        crud.award_xp("health_meal", xp_result["xp"], user_id=user_id)
        
        print("✅ Meal logged successfully")
        print(f"🎮 {xp_result['details']}")
        return health_log
    except Exception as e:
        print(f"❌ Error logging meal: {e}")
    finally:
        db_session.close()

def log_water_intake(water_liters: float , user_id : int):
    """
    Log water intake. Can be called multiple times a day, adding to the daily total.
    """
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if we already have a health log for today
        existing_log = db_session.query(HealthLog).filter(
            HealthLog.date >= today,
            HealthLog.date < today + timedelta(days=1),
            HealthLog.user_id == user_id
        ).order_by(HealthLog.date.desc()).first()
        
        # Use existing values or defaults
        sleep_hours = existing_log.sleep_hours if existing_log else 0.0
        exercise_minutes = existing_log.exercise_minutes if existing_log else 0
        meals = existing_log.meals if existing_log else ""
        
        # For water, we add to the existing amount
        water_intake = (existing_log.water_intake_liter if existing_log else 0.0) + water_liters
        
        # Store health data
        health_log = crud.create_health_log(
            user_id=user_id,
            db=db_session,
            meals=meals,
            sleep_hours=sleep_hours,
            water_intake_liter=water_intake,
            exercise_minutes=exercise_minutes
        )
        
        # Calculate and award XP immediately for this water intake
        from tools.xp_calculator import calculateXp
        xp_result = calculateXp(event_type="health", metrics={
            "water_intake_liters": water_liters,
            "activity_type": "water",
            "total_water_today": water_intake
        })
        
        # Award XP immediately
        crud.award_xp("health_water", xp_result["xp"], user_id=user_id)
        
        print(f"✅ Water intake logged: {water_liters}L (Daily total: {water_intake}L)")
        print(f"🎮 {xp_result['details']}")
        return health_log
    except Exception as e:
        print(f"❌ Error logging water intake: {e}")
    finally:
        db_session.close()

def log_sleep(hours: float , user_id : int):
    """
    Log sleep hours. Intended to be called once per day.
    """
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if we already have a health log for today
        existing_log = db_session.query(HealthLog).filter(
            HealthLog.user_id == user_id,
            HealthLog.date >= today,
            HealthLog.date < today + timedelta(days=1)
        ).order_by(HealthLog.date.desc()).first()
        
        # Use existing values or defaults
        water_intake = existing_log.water_intake_liter if existing_log else 0.0
        exercise_minutes = existing_log.exercise_minutes if existing_log else 0
        meals = existing_log.meals if existing_log else ""
        
        # Store health data
        health_log = crud.create_health_log(
            user_id = user_id,
            db=db_session,
            meals=meals,
            sleep_hours=hours,
            water_intake_liter=water_intake,
            exercise_minutes=exercise_minutes
        )
        
        # Calculate and award XP immediately for sleep
        from tools.xp_calculator import calculateXp
        xp_result = calculateXp(event_type="health", metrics={
            "sleep_hours": hours,
            "activity_type": "sleep"
        })
        
        # Award XP immediately
        crud.award_xp("health_sleep", xp_result["xp"], user_id=user_id)
        
        print(f"✅ Sleep logged: {hours} hours")
        print(f"🎮 {xp_result['details']}")
        return health_log
    except Exception as e:
        print(f"❌ Error logging sleep: {e}")
    finally:
        db_session.close()

def log_exercise(minutes: int , user_id : int):
    """
    Log exercise duration in minutes. Intended to be called once per day.
    """
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if we already have a health log for today
        existing_log = db_session.query(HealthLog).filter(
            HealthLog.user_id == user_id,
            HealthLog.date >= today,
            HealthLog.date < today + timedelta(days=1)
        ).order_by(HealthLog.date.desc()).first()
        
        # Use existing values or defaults
        water_intake = existing_log.water_intake_liter if existing_log else 0.0
        sleep_hours = existing_log.sleep_hours if existing_log else 0.0
        meals = existing_log.meals if existing_log else ""
        
        # Store health data
        health_log = crud.create_health_log(
            user_id=user_id,
            db=db_session,
            meals=meals,
            sleep_hours=sleep_hours,
            water_intake_liter=water_intake,
            exercise_minutes=minutes
        )
        
        # Calculate and award XP immediately for exercise
        from tools.xp_calculator import calculateXp
        xp_result = calculateXp(event_type="health", metrics={
            "exercise_minutes": minutes,
            "activity_type": "exercise"
        })
        
        # Award XP immediately
        crud.award_xp("health_exercise", xp_result["xp"], user_id=user_id)
        
        print(f"✅ Exercise logged: {minutes} minutes")
        print(f"🎮 {xp_result['details']}")
        return health_log
    except Exception as e:
        print(f"❌ Error logging exercise: {e}")
    finally:
        db_session.close()


def run_health_agent(user_id : int):
    """
    Calculate XP for all unprocessed health logs.
    This function is called by the scheduler.
    """
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if XP has already been awarded for health today
        xp_awarded = db_session.query(XPEvent).filter(
            XPEvent.user_id == user_id,
            XPEvent.timestamp >= today,
            XPEvent.xp_type == "health"
        ).fir
        
        if xp_awarded:
            print(f"⚠️ Health XP already awarded today ({xp_awarded.amount} XP). Skipping.")
            return
        
        # Get unprocessed health logs from today
        health_logs = db_session.query(HealthLog).filter(
            HealthLog.user_id == user_id,
            HealthLog.date >= today,
            HealthLog.processed == False
        ).order_by(HealthLog.date).all()
        
        if not health_logs:
            print("ℹ️ No unprocessed health logs found for today. No XP awarded.")
            return
        
        # For calculating XP, we'll use the most recent log of the day
        # which should contain the cumulative data for the day
        latest_log = health_logs[-1]
        
        # Score meals
        meal_score = score_meal_sentiment(latest_log.meals)
        
        # Calculate XP
        metrics = {
            "sleep_hours": latest_log.sleep_hours,
            "water_intake_liters": latest_log.water_intake_liter,
            "exercise_minutes": latest_log.exercise_minutes,
            "meal_score": meal_score,
            "meals": latest_log.meals
        }
        
        xp_result = calculateXp(event_type="health", metrics=metrics)
        total_xp = xp_result["xp"]
        
        # Mark all logs as processed
        for log in health_logs:
            log.processed = True
            log.processed_at = datetime.now()
        
        # Award XP for the day
        crud.award_xp("health", total_xp , user_id)
        db_session.commit()
        
        print(f"🧠 Daily Health XP Awarded: +{total_xp} XP")
        
    except Exception as e:
        print(f"❌ Error calculating health XP: {e}")
        db_session.rollback()
    finally:
        db_session.close()
