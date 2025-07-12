from apscheduler.schedulers.background import BackgroundScheduler
from app.agents.mood_agent import  calculate_daily_mood_xp
from app.db.database import get_db
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()


def run_all_daily_tasks():
    with next(get_db()) as db:
        print("🧠 Running daily XP + report tasks...")
        calculate_daily_mood_xp()
        

def start():
    scheduler.add_job(run_all_daily_tasks, 'cron', hour=23, minute=59)
    scheduler.start()