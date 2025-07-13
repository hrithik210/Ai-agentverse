from apscheduler.schedulers.background import BackgroundScheduler
from app.agents.mood_agent import calculate_daily_mood_xp
from app.agents.code_agent import run_code_agent
from app.agents.health_agent import run_health_agent
from app.agents.daily_report_agent import build_daily_report
from app.db.database import get_db_session
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()


def run_all_daily_tasks():
    print("🧠 Running daily tasks...")
    print("🧠 Running daily XP + report tasks...")
    
    # Each agent function manages its own database session
    try:
        calculate_daily_mood_xp()
    except Exception as e:
        print(f"Error in mood agent: {e}")
        
    try:
        run_code_agent()
    except Exception as e:
        print(f"Error in code agent: {e}")
        
    try:
        run_health_agent()
    except Exception as e:
        print(f"Error in health agent: {e}")
    
    # For the daily report, we need to pass a session
    try:
        db = get_db_session()
        if db:
            build_daily_report(db)
            db.close()
        else:
            print("Failed to get database session for daily report")
    except Exception as e:
        print(f"Error in daily report agent: {e}")


def start():
    # scheduler.add_job(run_all_daily_tasks, 'cron', hour=23, minute=59)
    scheduler.add_job(run_all_daily_tasks, 'interval', seconds=10)
    scheduler.start()