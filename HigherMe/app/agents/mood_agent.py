from app.db import crud
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()


#initializing llm
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    # other params...
)

def analyze_mood_sentiment(text: str) -> float:
  prompt = f"""
    On a scale from -1 (very negative) to 1 (very positive), rate the emotional tone of this journal entry.
    Only return a float. No words. Example: -0.6

    Entry: "{text}"
    """
  
  try:
    response = llm.invoke(prompt)
    sentiment_score = float(response.content.strip())
    return sentiment_score
  
  except Exception as e:
    print(f"Error analyzing mood sentiment: {e}")
    return 0.0
  

def run_mood_agent(mood_text: str):
    """
    Log a mood entry. XP is calculated on a schedule at end of day.
    """
    sentiment_score = analyze_mood_sentiment(mood_text)

    # Log mood entry
    crud.create_mood_log(
        mood_text=mood_text,
        sentiment=sentiment_score
    )
    
    print(f"✅ Mood logged with sentiment score: {sentiment_score}")
    print("📊 Mood XP will be calculated at the end of the day.")

def calculate_daily_mood_xp():
    """
    Calculate XP for all mood logs from today.
    This function should be scheduled to run once daily (e.g., at 11 PM).
    """
    from datetime import datetime
    from app.tools.xp_calculator import calculateXp
    from app.db.database import get_db_session
    from app.db.models import MoodLog, XPEvent
    
    # Use a session to get mood logs
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if XP has already been awarded for mood today
        xp_awarded = db_session.query(XPEvent).filter(
            XPEvent.timestamp >= today,
            XPEvent.xp_type == "mood"
        ).first()
        
        if xp_awarded:
            print(f"⚠️ Mood XP already awarded today ({xp_awarded.amount} XP). Skipping.")
            return
        
        # Get today's mood logs
        mood_logs = db_session.query(MoodLog).filter(
            MoodLog.timestamp >= today
        ).order_by(MoodLog.timestamp).all()
        
        if not mood_logs:
            print("ℹ️ No mood logs found for today. No XP awarded.")
            return
        
        # Calculate XP
        xp_result = calculateXp(event_type="mood", metrics={"mood_logs": mood_logs})
        
        # Use our new CRUD function for XP
        from app.db import crud
        crud.award_daily_xp("mood", xp_result["xp"])
        
        print(f"🧠 Daily Mood XP Awarded: +{xp_result['xp']} XP")
        if 'details' in xp_result:
            print(f"📝 {xp_result['details']}")
        
    except Exception as e:
        print(f"❌ Error calculating mood XP: {e}")
    finally:
        db_session.close()