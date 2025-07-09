from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.db.models import XPEvent, MoodLog, HealthLog, CodeLog, Level
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
        HealthLog.date >= today,
        HealthLog.date < tomorrow
    ).all()

    code_logs = db.query(CodeLog).filter(
        CodeLog.date >= today,
        CodeLog.date < tomorrow
    ).all()

    level_info = db.query(Level).first()

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
        return "🧠 **Mood:** No mood logs today."

    combined = "\n".join([
        f"[{mood.timestamp.strftime('%H:%M')}] {mood.mood_text}"
        for mood in mood_logs
    ])

    prompt = f"""
Summarize today's emotional journey in 2-3 sentences. Be direct and encouraging, no poetry.

Mood logs:
{combined}

Focus on emotional patterns and growth.
"""

    try:
        response = llm.invoke(prompt).content.strip()
        return f"🧠 **Mood:** {response}"
    except Exception as e:
        return f"🧠 **Mood:** ❌ Failed to generate summary: {e}"


def build_health_summary(health_logs):
    if not health_logs:
        return "💪 **Health:** No health logs today."
    
    combined = "\n".join([
        f"Meals: {log.meals}, Sleep: {log.sleep_hours}h, Exercise: {log.exercise_minutes}min, Water: {log.water_intake_liter}L"
        for log in health_logs
    ])
    
    prompt = f"""
Summarize today's health activities in 2-3 sentences. Be direct and motivational.

Health logs:
{combined}

Focus on wellness patterns and achievements.
"""
    
    try:
        response = llm.invoke(prompt).content.strip()
        return f"💪 **Health:** {response}"
    except Exception as e:
        return f"💪 **Health:** ❌ Failed to generate summary: {e}"


def build_code_summary(code_logs):
    if not code_logs:
        return "⌨️ **Code:** No coding activity today."
    
    total_lines_added = sum(log.lines_added or 0 for log in code_logs)
    total_lines_removed = sum(log.lines_removed or 0 for log in code_logs)
    total_time = sum(log.total_time_minutes or 0 for log in code_logs)
    
    combined = f"Lines added: {total_lines_added}, Lines removed: {total_lines_removed}, Total time: {total_time:.1f} minutes"
    
    prompt = f"""
Summarize today's coding productivity in 2-3 sentences. Be direct and tech-savvy.

Coding stats:
{combined}

Focus on productivity and development progress.
"""
    
    try:
        response = llm.invoke(prompt).content.strip()
        return f"⌨️ **Code:** {response}"
    except Exception as e:
        return f"⌨️ **Code:** ❌ Failed to generate summary: {e}"


def build_overall_summary(mood_logs, health_logs, code_logs, xp_events):
    # Prepare context for overall summary
    mood_count = len(mood_logs)
    health_count = len(health_logs)
    code_count = len(code_logs)
    total_xp = sum(xp.amount for xp in xp_events)
    
    context = f"""
Today's activity:
- {mood_count} mood logs
- {health_count} health logs  
- {code_count} coding sessions
- {total_xp} total XP earned

Generate a brief overall summary (2-3 sentences) of today's performance across all areas. Be encouraging and direct.
"""
    
    try:
        response = llm.invoke(context).content.strip()
        return f"\n🎯 **Overall:** {response}"
    except Exception as e:
        return f"\n🎯 **Overall:** ❌ Failed to generate summary: {e}"



def build_daily_report(db: Session):
    logs = get_today_logs(db)
    
    # Generate section summaries
    xp_section = format_xp_breakdown(logs["xp_events"])
    mood_section = build_mood_summary(logs["mood_logs"])
    health_section = build_health_summary(logs["health_logs"])
    code_section = build_code_summary(logs["code_logs"])
    overall_section = build_overall_summary(
        logs["mood_logs"], 
        logs["health_logs"], 
        logs["code_logs"], 
        logs["xp_events"]
    )

    level_info = logs["level"]
    level_line = f"\n🧬 Current Level: {level_info.current_level} | Total XP: {level_info.total_xp}"

    report = "\n".join([
        "🌅 **Daily Report**",
        "-" * 30,
        xp_section,
        "",
        mood_section,
        "",
        health_section,
        "",
        code_section,
        overall_section,
        level_line
    ])

    return report