from app.db import crud
from sqlalchemy.orm import Session
from datetime import datetime
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from app.db.database import get_db_session
from app.db.models import MoodLog, XPEvent

load_dotenv()


# initializing llm
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
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

def log_mood(mood_text: str , user_id : int):
    """
    Log a mood entry and immediately calculate and award XP.
    Each mood log now earns XP instantly like a real gaming system.
    """
    db = get_db_session()
    try:
        sentiment_score = analyze_mood_sentiment(mood_text)
        
        # Log mood entry
        mood_log = crud.create_mood_log(
            db=db,
            mood_text=mood_text,
            sentiment=sentiment_score,
            user_id= user_id
        )
        
        if mood_log:
            print(f"✅ Mood logged with sentiment score: {sentiment_score}")
            
            # Calculate XP for this specific mood entry
            from app.tools.xp_calculator import calculateXp
            xp_result = calculateXp(event_type="mood", metrics={"sentiment_score": sentiment_score, "mood_text": mood_text})
            
            # Award XP immediately
            crud.award_xp("mood", xp_result["xp"], user_id=user_id)
            
            # Mark this log as processed since we've already awarded XP
            mood_log.processed = True
            mood_log.processed_at = datetime.now()
            db.add(mood_log)
            db.commit()
            
            print(f"🎮 {xp_result['details']}")
            return mood_log
        else:
            print("❌ Failed to log mood")
            return None
    except Exception as e:
        print(f"Error logging mood: {e}")
        return None
    finally:
        db.close()

def calculate_daily_mood_xp(user_id: int):
    """
    Calculate XP for all unprocessed mood logs.
    This function is called by the scheduler.
    """
    from app.tools.xp_calculator import calculateXp
    
    db = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if XP has already been awarded for mood today
        xp_awarded = db.query(XPEvent).filter(
            XPEvent.user_id == user_id,
            XPEvent.timestamp >= today,
            XPEvent.xp_type == "mood"
        ).first()
        
        if xp_awarded:
            print(f"⚠️ Mood XP already awarded today ({xp_awarded.amount} XP). Skipping.")
            return
        
        # Get unprocessed mood logs from today
        mood_logs = db.query(MoodLog).filter(
            MoodLog.user_id == user_id,
            MoodLog.timestamp >= today,
            MoodLog.processed == False
        ).order_by(MoodLog.timestamp).all()
        
        if not mood_logs:
            print("ℹ️ No unprocessed mood logs found for today. No XP awarded.")
            return
        
        # Calculate XP
        xp_result = calculateXp(event_type="mood", metrics={"mood_logs": mood_logs})
        
        # Award XP
        crud.award_xp("mood", xp_result["xp"] , user_id=user_id)
        
        # Update processed status
        now = datetime.now()
        for log in mood_logs:
            log.processed = True
            log.processed_at = now
        db.commit()
        
        print(f"🧠 Daily Mood XP Awarded: +{xp_result['xp']} XP")
        if 'details' in xp_result:
            print(f"📝 {xp_result['details']}")
        
    except Exception as e:
        print(f"❌ Error calculating mood XP: {e}")
        db.rollback()
    finally:
        db.close()