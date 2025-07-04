from app.db import crud
from app.tools.xp_calculator import calculateXp
from datetime import datetime
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()

#initializing llm
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    # other params...
)

def score_meal_sentiment(meal_text: str) -> float:
    prompt = f"""
      Rate the healthiness of this meal on a scale from -1 to 1. 
      Only return a number, no explanation.

      Meal: {meal_text}
      """
    try:
        result = llm(prompt).strip()
        return float(result)
    except Exception:
        return 0.0 
      
def run_health_agent(meals: str, sleep_hours: float, water_liters: float, exercise_minutes: int):
    meal_score = score_meal_sentiment(meals)

    # Store health data
    crud.create_health_log(
        meals=meals,
        sleep_hours=sleep_hours,
        water_intake_liter=water_liters,
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
    
    crud.create_xp_event(xp_type='health', amount=xp_result['xp'])
    level = crud.get_or_create_level()
    crud.update_level(new_xp=xp_result["xp"])
    
    print(f"✅ HealthAgent XP Summary:\n{xp_result['details']}")
