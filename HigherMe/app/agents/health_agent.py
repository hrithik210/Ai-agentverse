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