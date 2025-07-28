from apscheduler.schedulers.background import BackgroundScheduler
from app.agents.mood_agent import calculate_daily_mood_xp
from app.agents.code_agent import run_code_agent
from app.agents.health_agent import run_health_agent
from app.agents.daily_report_agent import build_daily_report
from app.db.database import get_db_session
from app.db.models import User
from sqlalchemy.orm import Session
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()


def run_all_daily_tasks():
    print("🧠 Running daily tasks...")
    print("🧠 Running daily XP + report tasks...")
    
    db = get_db_session()

    if not db:
        print("count not get current db session")
        return
    
    active_users = db.query(User).filter(User.is_active == True).all()
    
    for user in active_users:
        try:
            print(f"found {len(active_users)} active users")
            calculate_daily_mood_xp(user.id)
            run_code_agent(user.id)
            run_health_agent(user.id)
            build_daily_report(db , user.id)
        except Exception as e:
            print(f"error processing daily task , error : {e}")
        
    

def start():
    scheduler.add_job(run_all_daily_tasks, 'cron', hour=23, minute=30)
    scheduler.start()