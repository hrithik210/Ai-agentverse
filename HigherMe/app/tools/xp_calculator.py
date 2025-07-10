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
    
    # Handle specific event types with dedicated calculators
    if event_type == "mood" and "mood_logs" in metrics:
        return _calculate_mood_performance_xp(metrics["mood_logs"])
        
    if event_type == "health":
        return _calculate_health_xp(metrics)
        
    if event_type == "coding":
        return _calculate_coding_xp(metrics)
    
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
- IMPORTANT: Evaluate overall health with MAX of 30 XP for excellent health habits

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

def _calculate_health_xp(metrics: dict) -> dict:
    """Calculates XP for health metrics in a consistent way"""
    sleep = metrics.get("sleep_hours", 0)
    water = metrics.get("water_intake_liters", 0)
    exercise = metrics.get("exercise_minutes", 0)
    meal_score = metrics.get("meal_score", 0)
    
    # Calculate health score on scale of 0-10
    health_score = 0
    if sleep >= 7: health_score += 2.5
    if water >= 2: health_score += 2.5
    if exercise >= 30: health_score += 2.5
    health_score += (meal_score + 1) * 1.25  # Convert -1 to 1 scale to 0 to 2.5 scale
    
    # Cap at maximum of 10 and convert to 0-30 XP range
    health_score = min(10, health_score)
    xp = int(health_score * 3)
    
    return {
        "xp": xp,
        "details": f"🏋️ Health XP: +{xp} (Overall health score: {health_score:.1f}/10)"
    }

def _fallback_xp_calculation(event_type: str, metrics: dict) -> dict:
    """Fallback XP calculation if LLM fails"""
    xp = 0
    details = ""
    
    if event_type == 'coding':
        result = _calculate_coding_xp(metrics)
        xp = result["xp"]
        details = result["details"]
    
    elif event_type == "health":
        result = _calculate_health_xp(metrics)
        xp = result["xp"]
        details = result["details"]
         
    elif event_type == "mood":
        # If we have mood_logs, use the proper calculator
        if "mood_logs" in metrics:
            result = _calculate_mood_performance_xp(metrics["mood_logs"])
            xp = result["xp"]
            details = result["details"]
        # Otherwise fallback to sentiment score only
        else:
            sentiment = metrics.get("sentiment_score", 0)
            xp = int((sentiment + 1) * 15)  # -1 to 1 → 0 to 30 XP
            details = f"🧠 Mood XP: +{xp} (based on sentiment score)"
    
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
rate the overall emotional performance on a scale from 0 to 30.

Consider:
- Self-reflection and awareness
- Emotional range and growth
- Coping with challenges
- Overall mood trajectory

Respond with ONLY this JSON format:
{"xp": <number>, "details": "<brief motivational explanation>"}

Example: {"xp": 20, "details": "🧠 Strong emotional awareness! Great self-reflection and positive growth."}
"""

    try:
        response = llm.invoke(prompt)
        import json
        result = json.loads(response.content.strip())
        
        xp = max(0, min(30, int(result.get("xp", 0))))  # 0-30 scale for consistency with health
        details = result.get("details", f"🧠 Emotional performance XP: +{xp}")
        
        return {"xp": xp, "details": details}
        
    except Exception as e:
        print(f"⚠️ LLM mood performance calculation failed: {e}")
        # Fallback: average sentiment-based calculation
        if mood_logs:
            avg_sentiment = sum(log.sentiment for log in mood_logs) / len(mood_logs)
            xp = int((avg_sentiment + 1) * 15)  # -1 to 1 → 0 to 30
        else:
            xp = 0
        return {"xp": xp, "details": f"🧠 Mood XP: +{xp} (fallback calculation)"}

def _calculate_coding_xp(metrics: dict) -> dict:
    """Calculates XP for coding metrics in a consistent way"""
    lines_added = metrics.get('lines_added', 0)
    lines_removed = metrics.get('lines_removed', 0)
    total_lines = lines_added + lines_removed
    minutes = metrics.get('total_time_minutes', 0)
    
    # Base XP calculation
    lines_xp = total_lines // 10  # 10 lines = 1 XP
    time_xp = minutes // 10       # 10 minutes = 1 XP
    
    # Calculate coding score with some weight adjustments
    # Focus more on time spent coding than just raw line count
    coding_xp = min(50, int(time_xp * 0.7 + lines_xp * 0.3))
    
    # Add bonus for significant coding sessions
    if minutes >= 120:  # 2+ hours coding
        coding_xp += 5
        details = f"💻 Coding XP: +{coding_xp} (Great coding session with {total_lines} lines over {minutes} minutes!)"
    else:
        details = f"💻 Coding XP: +{coding_xp} ({total_lines} lines over {minutes} minutes)"
    
    return {
        "xp": coding_xp,
        "details": details
    }