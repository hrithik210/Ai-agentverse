
from app.db.database import get_db, get_db_session
from app.agents.mood_agent import run_mood_agent
from app.tools.xp_calculator import calculate_mood_performance_xp
from app.db.models import MoodLog
from datetime import datetime

def seed_mood_logs(db):
    print("🌤️ Logging today's moods...")
    run_mood_agent("Woke up feeling meh, dragged through the morning.", db)
    run_mood_agent("Got into flow around lunch, banged out some code.", db)
    run_mood_agent("Had a nice walk, feeling calm and clear-headed.", db)

def test():
    # Use raw connection for mood agent (CRUD operations)
    db_conn = get_db()
    # Use SQLAlchemy session for ORM operations
    db_session = get_db_session()
    
    if db_conn and db_session:
        try:
            # STEP 1: Log multiple moods (uses raw connection)
            seed_mood_logs(db_conn)

            # STEP 2: Get today's mood logs and calculate XP using new calculator
            print("\n📈 Running Mood XP Calculator...")
            today = datetime.now().date()
            mood_logs = db_session.query(MoodLog).filter(MoodLog.timestamp >= today).order_by(MoodLog.timestamp).all()
            xp = calculate_mood_performance_xp(mood_logs, db_session)

            # STEP 3: Show result
            print(f"\n✅ Test complete. Mood XP awarded: {xp}")
        finally:
            db_conn.close()
            db_session.close()

if __name__ == "__main__":
    test()