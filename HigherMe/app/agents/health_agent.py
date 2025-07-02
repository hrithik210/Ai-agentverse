from app.db import crud
from app.tools.xp_calculator import calculateXp
from app.db.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime

def score_meal_sentiment(meal_text: str) -> float:
    prompt = f"""
    Rate the nutritional healthiness of this meal on a scale from -1 (very unhealthy) to 1 (very healthy).
    Only return the number. No text.
    
    Meals: "{meal_text}"
    """
    try:
        result = llm(prompt).strip()
        return float(result)
    except Exception:
        return 0.0 
      
def run_health_agent(meals: str, sleep_hours: float, water_liters: float, exercise_minutes: float, db: Session):
    meal_score = score_meal_sentiment(meals)

    # Store health data
    crud.create_health_log(
        db=db,
        meals=meals,
        sleep_hours=sleep_hours,
        water_intake_liters=water_liters,
        exercise_minutes=exercise_minutes
    )

    # XP calculation
    metrics = {
        "sleep_hours": sleep_hours,
        "water_intake_liters": water_liters,
        "exercise_minutes": exercise_minutes,
        "meal_score": meal_score,
        "meals": meals
    }

    xp_result = calculateXp(event_type="health", metrics=metrics)
    
    crud.create_xp_event()
