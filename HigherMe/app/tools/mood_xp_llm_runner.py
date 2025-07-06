
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import crud
from app.db.models import MoodLog
from dotenv import load_dotenv
import os
from langchain_groq import ChatGroq


load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
    # other params...
)

def get_today_mood_logs(db: Session):
    today = datetime.utcnow().date()
    return db.query(MoodLog).filter(MoodLog.timestamp >= today).order_by(MoodLog.timestamp).all()
  

def build_prompt(mood_logs):
    if not mood_logs:
        return "No mood logs for today. Return 0."

    prompt = """You are an emotional coach tracking my mental state.

Here are my mood logs for the day:\n"""

    for log in mood_logs:
        timestamp = log.timestamp.strftime("%H:%M")
        prompt += f"- [{timestamp}] \"{log.mood_text}\"\n"

    prompt += """
Based on my emotional awareness, resilience, and progress today,
rate my emotional performance on a scale from 0 to 10.

Return ONLY the number. No explanation.
"""
    return prompt
  
  
def run_mood_xp_llm_runner(db: Session):
    mood_logs = get_today_mood_logs(db)
    prompt = build_prompt(mood_logs)

    try:
        raw_response = llm.invoke(prompt).content.strip()
        xp = int(float(raw_response))  # safely cast to int
    except Exception as e:
        print(f"⚠️ Failed to get LLM XP: {e}")
        xp = 0

    # Store XP
    crud.create_xp_event(xp_type="mood", amount=xp)
    crud.update_level(new_xp=xp)

    print(f"🧠 LLM-Based Mood XP: +{xp} XP awarded for today.")

    return xp