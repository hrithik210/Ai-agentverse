from app.db.database import get_db
from app.agents.health_agent import run_health_agent

def test():
    with next(get_db()) as db:
        run_health_agent(
            meals="breakfast: oats and banana, lunch: grilled chicken and salad, dinner: paneer wrap",
            sleep_hours=7.5,
            exercise_minutes=45,
            water_liters=2.0,
            db=db
        )

if __name__ == "__main__":
    test()
