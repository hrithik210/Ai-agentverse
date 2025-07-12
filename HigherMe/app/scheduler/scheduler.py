from apscheduler.schedulers.background import BackgroundScheduler
from app.agents import mood_xp_llm_runner, health_xp_runner, code_xp_runner, daily_report_agent
from app.db.database import get_db
import logging

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)

scheduler = BackgroundScheduler()