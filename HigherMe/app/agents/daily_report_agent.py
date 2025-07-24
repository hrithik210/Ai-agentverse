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

def get_today_logs(db: Session , user_id : int):
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    xp_events = db.query(XPEvent).filter(
        XPEvent.user_id == user_id,
        XPEvent.timestamp >= today,
        XPEvent.timestamp < tomorrow
    ).all()

    mood_logs = db.query(MoodLog).filter(
        MoodLog.user_id == user_id,
        MoodLog.timestamp >= today,
        MoodLog.timestamp < tomorrow
    ).all()

    health_logs = db.query(HealthLog).filter(
        HealthLog.user_id == user_id,
        HealthLog.date >= today,
        HealthLog.date < tomorrow
    ).all()

    code_logs = db.query(CodeLog).filter(
        CodeLog.user_id == user_id,
        CodeLog.date >= today,
        CodeLog.date < tomorrow
    ).all()

    level_info = db.query(Level).filter(Level.user_id == user_id).first()

    return {
        "xp_events": xp_events,
        "mood_logs": mood_logs,
        "health_logs": health_logs,
        "code_logs": code_logs,
        "level": level_info
    }
    
def format_xp_breakdown(xp_events):
    summary = {}
    details = {}
    total = 0

    for xp in xp_events:
        xp_type = xp.xp_type
        summary[xp_type] = summary.get(xp_type, 0) + xp.amount
        total += xp.amount
        
        # Store details for each XP type
        if xp.details:
            details[xp_type] = xp.details

    lines = [f"🔢 **XP Breakdown:**"]
    for key, value in summary.items():
        lines.append(f"- {key.capitalize()}: +{value} XP")
    lines.append(f"\n🏆 **Total XP Today:** +{total}")
    
    return "\n".join(lines), details


def build_mood_summary(mood_logs, xp_details):
    if not mood_logs:
        return "🧠 **Mood:** No mood logs today."

    # Use XP details if available, otherwise fallback to basic summary
    if xp_details:
        prompt = f"""
Based on the mood XP analysis, create a brief summary (2-3 sentences) of today's emotional progress. Be encouraging and insightful.

Mood XP Details: {xp_details}

Focus on emotional growth and awareness patterns.
"""
        try:
            response = llm.invoke(prompt).content.strip()
            return f"🧠 **Mood:** {response}"
        except Exception as e:
            return f"🧠 **Mood:** ❌ Failed to generate summary: {e}"
    else:
        # Fallback to basic count
        return f"🧠 **Mood:** {len(mood_logs)} mood entries logged today."


def build_health_summary(health_logs, xp_details):
    if not health_logs:
        return "💪 **Health:** No health logs today."
    
    # Use XP details if available, otherwise fallback to basic summary
    if xp_details:
        prompt = f"""
Based on the health XP analysis, create a brief summary (2-3 sentences) of today's wellness activities. Be motivational and specific.

Health XP Details: {xp_details}

Focus on health achievements and areas of improvement.
"""
        try:
            response = llm.invoke(prompt).content.strip()
            return f"💪 **Health:** {response}"
        except Exception as e:
            return f"💪 **Health:** ❌ Failed to generate summary: {e}"
    else:
        # Fallback to basic count
        return f"💪 **Health:** {len(health_logs)} health entries logged today."


def build_code_summary(code_logs, xp_details):
    if not code_logs:
        return "⌨️ **Code:** No coding activity today."
    
    # Use XP details if available, otherwise fallback to basic summary
    if xp_details:
        prompt = f"""
Based on the coding XP analysis, create a brief summary (2-3 sentences) of today's development work. Be tech-focused and encouraging.

Coding XP Details: {xp_details}

Focus on productivity and coding achievements.
"""
        try:
            response = llm.invoke(prompt).content.strip()
            return f"⌨️ **Code:** {response}"
        except Exception as e:
            return f"⌨️ **Code:** ❌ Failed to generate summary: {e}"
    else:
        # Fallback to basic count
        return f"⌨️ **Code:** {len(code_logs)} coding sessions logged today."


def build_overall_summary(mood_logs, health_logs, code_logs, xp_events, xp_details):
    # Prepare context for overall summary
    mood_count = len(mood_logs)
    health_count = len(health_logs)
    code_count = len(code_logs)
    total_xp = sum(xp.amount for xp in xp_events)
    
    # Include XP details in the context if available
    details_context = ""
    if xp_details:
        details_lines = []
        for xp_type, details in xp_details.items():
            details_lines.append(f"- {xp_type.capitalize()}: {details}")
        details_context = f"\n\nXP Analysis Details:\n" + "\n".join(details_lines)
    
    context = f"""
Today's activity summary:
- {mood_count} mood logs
- {health_count} health logs  
- {code_count} coding sessions
- {total_xp} total XP earned{details_context}

Generate a brief overall summary (2-3 sentences) of today's performance across all areas. Be encouraging, specific, and highlight key achievements or areas for improvement based on the XP analysis.
"""
    
    try:
        response = llm.invoke(context).content.strip()
        return f"\n🎯 **Overall:** {response}"
    except Exception as e:
        return f"\n🎯 **Overall:** ❌ Failed to generate summary: {e}"



def build_daily_report(db: Session , user_id : int):
    logs = get_today_logs(db, user_id)
    
    # Generate XP breakdown and extract details
    xp_section, xp_details = format_xp_breakdown(logs["xp_events"])
    
    # Generate section summaries using XP details
    mood_section = build_mood_summary(logs["mood_logs"], xp_details.get("mood"))
    health_section = build_health_summary(logs["health_logs"], xp_details.get("health"))
    code_section = build_code_summary(logs["code_logs"], xp_details.get("code"))
    overall_section = build_overall_summary(
        logs["mood_logs"], 
        logs["health_logs"], 
        logs["code_logs"], 
        logs["xp_events"],
        xp_details
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
    print("📄 Daily report generated successfully.")
    print(report)
    return report