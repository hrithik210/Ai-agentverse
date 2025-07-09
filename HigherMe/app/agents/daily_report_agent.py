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
    
def format_xp_breakdown(xp_events):
    summary = {}
    total = 0

    for xp in xp_events:
        summary[xp.xp_type] = summary.get(xp.xp_type, 0) + xp.amount
        total += xp.amount

    lines = [f"🔢 **XP Breakdown:**"]
    for key, value in summary.items():
        lines.append(f"- {key.capitalize()}: +{value} XP")
    lines.append(f"\n🏆 **Total XP Today:** +{total}")
    return "\n".join(lines)


def build_mood_summary(mood_logs):
    if not mood_logs:
        return "🧠 No mood logs today."

    combined = "\n".join([
        f"[{mood.timestamp.strftime('%H:%M')}] {mood.mood_text}"
        for mood in mood_logs
    ])

    prompt = f"""
You are an AI narrator summarizing emotional growth.

Here are the mood reflections from today:

{combined}

Give a short emotional summary of the day. Be supportive and slightly poetic.
"""

    try:
        return llm.invoke(prompt).strip()
    except Exception as e:
        return f"❌ Failed to generate mood summary: {e}"



def build_daily_report(db: Session):
    logs = get_today_logs(db)
    xp_section = format_xp_breakdown(logs["xp_events"])
    mood_section = build_mood_summary(logs["mood_logs"])

    level_info = logs["level"]
    level_line = f"\n🧬 Current Level: {level_info.level} | Total XP: {level_info.total_xp}"

    report = "\n".join([
        "🌅 **Daily Report**",
        "-" * 30,
        xp_section,
        "",
        mood_section,
        level_line
    ])

    return report