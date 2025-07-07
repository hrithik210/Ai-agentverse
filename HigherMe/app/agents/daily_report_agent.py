from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import XPEvent, MoodLog, HealthLog, CodeLog, UserLevel
from langchain.llms import Groq
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    # other params...
)

def get_today_logs(db: Session):
    today = datetime.utcnow().date()
    tomorrow = today + timedelta(days=1)

    xp_events = db.query(XPEvent).filter(
        XPEvent.timestamp >= today,
        XPEvent.timestamp < tomorrow
    ).all()

    mood_logs = db.query(MoodLog).filter(
        MoodLog.timestamp >= today,
        MoodLog.timestamp < tomorrow
    ).all()

    health_logs = db.query(HealthLog).filter(
        HealthLog.timestamp >= today,
        HealthLog.timestamp < tomorrow
    ).all()

    code_logs = db.query(CodeLog).filter(
        CodeLog.timestamp >= today,
        CodeLog.timestamp < tomorrow
    ).all()

    level_info = db.query(UserLevel).first()

    return {
        "xp_events": xp_events,
        "mood_logs": mood_logs,
        "health_logs": health_logs,
        "code_logs": code_logs,
        "level": level_info
    }