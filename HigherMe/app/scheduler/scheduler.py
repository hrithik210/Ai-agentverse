from apscheduler.schedulers.background import BackgroundScheduler
from app.agents.mood_agent import  calculate_daily_mood_xp
from app.agents.code_agent import run_code_agent
from app.agents.health_agent import run_health_agent

from app.agents.daily_report_agent import build_daily_report

from app.db.database import get_db
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()


def run_all_daily_tasks():
    with get_db() as db:
        print("🧠 Running daily tasks...")
        print("🧠 Running daily XP + report tasks...")
        calculate_daily_mood_xp()
        run_code_agent()
        run_health_agent()
        build_daily_report(db)
        
        

def start():
    # scheduler.add_job(run_all_daily_tasks, 'cron', hour=23, minute=59)
    scheduler.add_job(run_all_daily_tasks, 'interval', seconds=10)
    scheduler.start()