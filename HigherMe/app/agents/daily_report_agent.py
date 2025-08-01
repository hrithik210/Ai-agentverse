from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from db.models import XPEvent, MoodLog, HealthLog, CodeLog, Level
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
    print(f"Fetching today's logs for user {user_id}...")
    today = datetime.now().date()
    tomorrow = today + timedelta(days=1)

    xp_events = db.query(XPEvent).filter(
        XPEvent.user_id == user_id,
        XPEvent.timestamp >= today,
        XPEvent.timestamp < tomorrow
    ).all()
    print(f"Found {len(xp_events)} XP events for today.")
    mood_logs = db.query(MoodLog).filter(
        MoodLog.user_id == user_id,
        MoodLog.timestamp >= today,
        MoodLog.timestamp < tomorrow
    ).all()
    print(f"Found {len(mood_logs)} mood logs for today.")
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
    
    # Create level record if it doesn't exist
    if not level_info:
        print(f"⚠️ No level record found for user {user_id}. Creating one...")
        level_info = Level(
            user_id=user_id,
            current_level=1,
            total_xp=0,
            last_updated=datetime.now()
        )
        db.add(level_info)
        db.commit()
        db.refresh(level_info)
        print(f"✅ Created level record for user {user_id}")
    
    print(f"Fetched {len(xp_events)} XP events, {len(mood_logs)} mood logs, {len(health_logs)} health logs, and {len(code_logs)} code logs. , level info: {level_info}")
    return {
        "xp_events": xp_events,
        "mood_logs": mood_logs,
        "health_logs": health_logs,
        "code_logs": code_logs,
        "level": level_info
    }
    
def format_xp_breakdown(xp_events):
    print(f"🔢 Inside format_xp_breakdown - Processing {len(xp_events)} XP events")
    
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
            print(f"🔢 Added details for {xp_type}: {xp.details}")

    print(f"🔢 XP Summary: {summary}")
    print(f"🔢 XP Details: {details}")
    print(f"🔢 Total XP: {total}")

    lines = [f"🔢 **XP Breakdown:**"]
    for key, value in summary.items():
        lines.append(f"- {key.capitalize()}: +{value} XP")
    lines.append(f"\n🏆 **Total XP Today:** +{total}")
    
    formatted_breakdown = "\n".join(lines)
    print(f"🔢 Formatted XP breakdown: {formatted_breakdown}")
    
    return formatted_breakdown, details


def build_mood_summary(mood_logs, xp_details):
    print(f"🧠 Inside build_mood_summary - Processing {len(mood_logs)} mood logs")
    
    if not mood_logs:
        print("🧠 No mood logs found for today")
        return "🧠 **Mood:** No mood logs today."

    # First, try to use our enhanced mood summary function that leverages actual mood text
    try:
        # Import the enhanced mood summary function
        from agents.mood_summary import mood_summary_with_sentiment
        from datetime import datetime
        
        # Get the user_id from the first mood log (assuming all logs are from the same user)
        if mood_logs:
            user_id = mood_logs[0].user_id
            
            # Get today's date from the mood logs
            target_date = datetime.now().date()
            if mood_logs:
                # Use the date from the first mood log if available
                target_date = mood_logs[0].timestamp.date()
            
            # Generate enhanced summary using actual mood text for the specific date
            enhanced_summary = mood_summary_with_sentiment(user_id, target_date)
            
            if enhanced_summary and enhanced_summary["summary"] and "No mood entries" not in enhanced_summary["summary"] and "Unable to generate summary" not in enhanced_summary["summary"]:
                print(f"🧠 Using enhanced mood summary: {enhanced_summary['summary']}")
                return f"🧠 **Mood:** {enhanced_summary['summary']}"
            elif len(mood_logs) == 1 and mood_logs[0].mood_text:
                # Special case for single mood entry
                mood_text = mood_logs[0].mood_text
                simple_summary = f"Aha! You shared that you're feeling \"{mood_text[:30]}...\" today - thanks for letting me know!"
                print(f"🧠 Using simple mood summary for single entry: {simple_summary}")
                return f"🧠 **Mood:** {simple_summary}"
    except Exception as e:
        print(f"🧠 Error generating enhanced mood summary: {e}")
        # Continue with fallback approaches

    # Use XP details if available, otherwise fallback to basic summary
    if xp_details:
        print(f"🧠 Using XP details for mood summary: {xp_details}")
        prompt = f"""
You are a wise and grounded mentor. Based on the following XP analysis, write a brief (2-3 sentence) summary of today's emotional progress.

Avoid over-enthusiasm. Be realistic, encouraging, and thoughtful. Highlight emotional awareness, reflection, and meaningful changes.

Mood XP Details: {xp_details}
"""
        try:
            response = llm.invoke(prompt).content.strip()
            print(f"🧠 Generated mood summary: {response}")
            return f"🧠 **Mood:** {response}"
        except Exception as e:
            print(f"🧠 Error generating mood summary: {e}")
            return f"🧠 **Mood:** ❌ Failed to generate summary: {e}"
    else:
        # Fallback to basic count with more detail
        mood_texts = [log.mood_text for log in mood_logs if log.mood_text]
        if mood_texts:
            # Create a more meaningful summary from actual mood texts
            prompt = f"""
You are a friendly, witty, and empathetic companion who understands human emotions deeply. Based on the following mood journal entries from a single day, write a concise 2-3 sentence summary that captures the emotional journey of the day in a warm, relatable way.

Instructions:
- Be silly, witty, empathic, and considerate
- Use casual, friendly language that a close friend might use
- Focus on the human experience and emotional patterns
- Avoid technical terms like "sentiment" or "emotional stimuli"
- Keep it brief and readable

Mood Entries:
{chr(10).join(f'- "{text}"' for text in mood_texts[:5])}

Summary:"""
            
            try:
                response = llm.invoke(prompt).content.strip()
                if response:
                    print(f"🧠 Generated mood summary from actual entries: {response}")
                    return f"🧠 **Mood:** {response}"
            except Exception as e:
                print(f"🧠 Error generating mood summary from entries: {e}")
        
        # Ultimate fallback to basic count
        if len(mood_logs) == 1:
            fallback_summary = "🧠 **Mood:** Aha! You shared your mood today - thanks for letting me know!"
        else:
            fallback_summary = f"🧠 **Mood:** You shared {len(mood_logs)} mood updates today - that's awesome!"
        print(f"🧠 Using fallback mood summary: {fallback_summary}")
        return fallback_summary


def build_health_summary(health_logs, xp_details):
    print(f"💪 Inside build_health_summary - Processing {len(health_logs)} health logs")
    
    if not health_logs:
        print("💪 No health logs found for today")
        return "💪 **Health:** No health logs today."
    
    # First, try to use our enhanced health summary function that leverages actual health log strings
    try:
        # Import the enhanced health summary function
        from agents.health_summary import health_summary
        from datetime import datetime
        
        # Get the user_id from the first health log (assuming all logs are from the same user)
        if health_logs:
            user_id = health_logs[0].user_id
            today = datetime.now().date()
            
            # Generate summary using actual health log strings
            summary_text = health_summary(user_id, today)
            
            if summary_text and not summary_text.startswith("Unable to retrieve") and not summary_text.startswith("No health entries"):
                return f"💪 **Health:** {summary_text}"
            else:
                print(f"💪 Health summary function returned fallback: {summary_text}")
        
    except Exception as e:
        print(f"💪 Error using health summary function: {e}")
    
    # Fallback to XP details if available
    if xp_details:
        print(f"💪 Using XP details for health summary: {xp_details}")
        prompt = f"""
You are a friendly, witty, and empathetic health companion who understands that health journeys are personal and unique. Based on the health activities below, write a 2-3 sentence summary of today's health journey in a warm, encouraging way.

Instructions:
- Be silly, witty, empathic, and considerate
- Use casual, friendly language that a supportive friend might use
- Acknowledge effort and progress, no matter how small
- Celebrate wins and gently encourage continued growth
- Avoid technical terms and keep it relatable

Health Activities: {xp_details}
"""
        try:
            response = llm.invoke(prompt).content.strip()
            print(f"💪 Generated health summary from XP details: {response}")
            if response:
                return f"💪 **Health:** {response}"
            else:
                # Fallback if LLM returns empty response
                if len(health_logs) == 1:
                    return "💪 **Health:** Nice work taking care of yourself today!"
                else:
                    return f"💪 **Health:** You focused on your health {len(health_logs)} times today - that's awesome!"
        except Exception as e:
            print(f"💪 Error generating health summary from XP details: {e}")
    
    # Ultimate fallback to basic summary
    if len(health_logs) == 1:
        fallback_summary = "💪 **Health:** Nice work taking care of yourself today!"
    else:
        fallback_summary = f"💪 **Health:** You focused on your health {len(health_logs)} times today - that's awesome!"
    print(f"💪 Using ultimate fallback health summary: {fallback_summary}")
    return fallback_summary


# def build_code_summary(code_logs, xp_details):
#     if not code_logs:
#         return "⌨️ **Code:** No coding activity today."
    
#     # Use XP details if available, otherwise fallback to basic summary
#     if xp_details:
#         prompt = f"""
# You're a pragmatic senior developer. Based on the XP analysis below, write a short (2–3 sentence) summary of today's coding session.

# Be realistic. Highlight actual effort, focus, and meaningful contributions. Skip hype — celebrate growth and progress with a mentor's tone.

# Coding XP Details: {xp_details}
# """
#         try:
#             response = llm.invoke(prompt).content.strip()
#             return f"⌨️ **Code:** {response}"
#         except Exception as e:
#             return f"⌨️ **Code:** ❌ Failed to generate summary: {e}"
#     else:
#         # Fallback to basic count
#         return f"⌨️ **Code:** {len(code_logs)} coding sessions logged today."


def build_overall_summary(mood_summary, health_summary, code_logs, xp_events, xp_details):
    print(f"🎯 Inside build_overall_summary - Processing overall summary")
    print(f"🎯 Mood summary: {mood_summary}")
    print(f"🎯 Health summary: {health_summary}")
    print(f"🎯 Code logs count: {len(code_logs)}")
    print(f"🎯 XP events count: {len(xp_events)}")
    print(f"🎯 XP details: {xp_details}")
    
    # Prepare context for overall summary
    total_xp = sum(xp.amount for xp in xp_events)
    print(f"🎯 Total XP calculated: {total_xp}")
    
    # Include XP details in the context if available
    details_context = ""
    if xp_details:
        details_lines = []
        for xp_type, details in xp_details.items():
            details_lines.append(f"- {xp_type.capitalize()}: {details}")
        details_context = f"\n\nXP Analysis Details:\n" + "\n".join(details_lines)
        print(f"🎯 XP details context: {details_context}")
    
    context = f"""
You are a wise accountability partner. Given this overview of today's activity, write a grounded, encouraging 2–3 sentence summary.

Avoid overhyping. Be real, constructive, and human. Mention what went well, and gently point out areas to improve.

Summary Data:
- Mood Activity: {mood_summary}
- Health Activity: {health_summary}  
- Code Sessions: {len(code_logs)} coding sessions
- Total XP Earned: {total_xp}{details_context}
"""
    
    print(f"🎯 Context for LLM: {context}")
    
    try:
        response = llm.invoke(context).content.strip()
        print(f"🎯 Generated overall summary: {response}")
        return f"\n🎯 **Overall:** {response}"
    except Exception as e:
        print(f"🎯 Error generating overall summary: {e}")
        return f"\n🎯 **Overall:** ❌ Failed to generate summary: {e}"



def build_daily_report(db: Session , user_id : int):
    print(f"📄 Starting daily report generation for user {user_id}")
    
    logs = get_today_logs(db, user_id)
    print(f"📄 Retrieved logs: {len(logs['xp_events'])} XP events, {len(logs['mood_logs'])} mood logs, {len(logs['health_logs'])} health logs, {len(logs['code_logs'])} code logs")
    
    # Generate XP breakdown and extract details
    print("📄 Generating XP breakdown...")
    xp_section, xp_details = format_xp_breakdown(logs["xp_events"])
    print(f"📄 XP section generated: {xp_section}")
    print(f"📄 XP details extracted: {xp_details}")
    
    # Generate section summaries using XP details
    print("📄 Building mood summary...")
    mood_section = build_mood_summary(logs["mood_logs"], xp_details.get("mood"))
    print(f"📄 Mood section result: {mood_section}")
    
    print("📄 Building health summary...")
    health_section = build_health_summary(logs["health_logs"], xp_details.get("health"))
    print(f"📄 Health section result: {health_section}")
    
    # code_section = build_code_summary(logs["code_logs"], xp_details.get("code"))
    
    print("📄 Building overall summary...")
    overall_section = build_overall_summary(
        mood_section, 
        health_section, 
        logs["code_logs"], 
        logs["xp_events"],
        xp_details
    )
    print(f"📄 Overall section result: {overall_section}")

    level_info = logs["level"]
    print(f"📄 Level info: {level_info}")
    
    # Handle case where user has no level record yet
    if level_info:
        level_line = f"\n🧬 Current Level: {level_info.current_level} | Total XP: {level_info.total_xp}"
    else:
        level_line = f"\n🧬 Current Level: 1 | Total XP: 0 (No level record found)"
    
    print(f"📄 Level line: {level_line}")

    report = "\n".join([
        "🌅 **Daily Report**",
        "-" * 30,
        xp_section,
        "",
        mood_section,
        "",
        health_section,
        "",
        overall_section,
        level_line
    ])
    return report