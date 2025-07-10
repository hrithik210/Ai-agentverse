from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq

load_dotenv()

# Initialize LLM for XP calculation
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
)

def calculateXp(event_type: str, metrics: dict) -> dict:
    """
    LLM-based XP calculation that considers context and effort.
    Returns a dict with XP amount and breakdown details.
    """
    
    # Handle mood logs specifically (like mood_xp_llm_runner)
    if event_type == "mood" and "mood_logs" in metrics:
        return _calculate_mood_performance_xp(metrics["mood_logs"])
    
    prompt = f"""You are a gamification expert calculating experience points (XP) for personal growth activities.

EVENT TYPE: {event_type}
METRICS: {metrics}

Based on the metrics provided, calculate appropriate XP (0-100 scale) considering:

For CODING:
- Lines of code added/removed (quality over quantity)
- Time spent (focus and productivity)
- Complexity and learning involved

For HEALTH:
- Sleep quality and duration (7-9 hours optimal)
- Water intake (2+ liters good)
- Exercise duration and intensity
- Meal quality and nutrition

For MOOD:
- Emotional awareness and reflection
- Sentiment improvement throughout day
- Self-care and mental health practices

RULES:
- Be fair but motivating
- Reward effort and consistency
- Consider realistic daily limits
- Higher XP for exceeding healthy baselines

Respond with ONLY this JSON format:
{{"xp": <number>, "details": "<brief motivational explanation>"}}

Example: {{"xp": 45, "details": "💻 Solid coding session! +45 XP for 2 hours of focused work and 150 lines."}}
"""

    try:
        response = llm.invoke(prompt)
        # Parse the JSON response
        import json
        result = json.loads(response.content.strip())
        
        # Ensure XP is within reasonable bounds
        xp = max(0, min(100, int(result.get("xp", 0))))
        details = result.get("details", f"XP calculated for {event_type}")
        
        return {
            "xp": xp,
            "details": details
        }
        
    except Exception as e:
        print(f"⚠️ LLM XP calculation failed: {e}")
        # Fallback to simple calculation
        return _fallback_xp_calculation(event_type, metrics)

def _fallback_xp_calculation(event_type: str, metrics: dict) -> dict:
    """Fallback XP calculation if LLM fails"""
    xp = 0
    details = ""
    
    if event_type == 'coding':
        lines = metrics.get('lines_added', 0) + metrics.get('lines_removed', 0)
        minutes = metrics.get('total_time_minutes', 0)
        xp = min(50, (lines // 10) + (minutes // 10))
        details = f"� Coding XP: +{xp} (fallback calculation)"
    
    elif event_type == "health":
        sleep = metrics.get("sleep_hours", 0)
        water = metrics.get("water_intake_liters", 0)
        exercise = metrics.get("exercise_minutes", 0)
        
        if sleep >= 7: xp += 20
        if water >= 2: xp += 10
        if exercise >= 30: xp += 15
        details = f"� Health XP: +{xp} (fallback calculation)"
         
    elif event_type == "mood":
        sentiment = metrics.get("sentiment_score", 0)
        xp = int((sentiment + 1) * 10)  # -1 to 1 → 0 to 20 XP
        details = f"🧠 Mood XP: +{xp} (fallback calculation)"
    
    return {"xp": xp, "details": details}

def _calculate_mood_performance_xp(mood_logs) -> dict:
    """
    Calculate XP based on overall emotional performance for the day.
    Similar to mood_xp_llm_runner but using the calculateXp pattern.
    """
    if not mood_logs:
        return {"xp": 0, "details": "🧠 No mood logs for today"}

    prompt = """You are an emotional coach tracking mental state performance.

Here are the mood logs for the day:\n"""

    for log in mood_logs:
        timestamp = log.timestamp.strftime("%H:%M")
        prompt += f"- [{timestamp}] \"{log.mood_text}\"\n"

    prompt += """
Based on emotional awareness, resilience, and progress today,
rate the overall emotional performance on a scale from 0 to 10.

Consider:
- Self-reflection and awareness
- Emotional range and growth
- Coping with challenges
- Overall mood trajectory

Respond with ONLY this JSON format:
{"xp": <number>, "details": "<brief motivational explanation>"}

Example: {"xp": 8, "details": "🧠 Strong emotional awareness! Great self-reflection and positive growth."}
"""

    try:
        response = llm.invoke(prompt)
        import json
        result = json.loads(response.content.strip())
        
        xp = max(0, min(10, int(result.get("xp", 0))))  # 0-10 scale like original
        details = result.get("details", f"🧠 Emotional performance XP: +{xp}")
        
        return {"xp": xp, "details": details}
        
    except Exception as e:
        print(f"⚠️ LLM mood performance calculation failed: {e}")
        # Fallback: average sentiment-based calculation
        if mood_logs:
            avg_sentiment = sum(log.sentiment for log in mood_logs) / len(mood_logs)
            xp = int((avg_sentiment + 1) * 5)  # -1 to 1 → 0 to 10
        else:
            xp = 0
        return {"xp": xp, "details": f"🧠 Mood XP: +{xp} (fallback calculation)"}

def calculate_mood_performance_xp(mood_logs, db_session=None):
    """
    Direct replacement for mood_xp_llm_runner.
    Takes mood logs and returns XP, optionally stores to database.
    """
    from app.db import crud
    
    result = _calculate_mood_performance_xp(mood_logs)
    xp = result["xp"]
    details = result["details"]
    
    # Store XP (like original mood_xp_llm_runner)
    if db_session:
        crud.create_xp_event(xp_type="mood", amount=xp)
        crud.update_level(new_xp=xp)
    
    print(f"🧠 LLM-Based Mood XP: +{xp} XP awarded for today.")
    print(f"Details: {details}")
    
    return xp