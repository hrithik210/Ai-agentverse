
from datetime import datetime
from sqlalchemy.orm import Session
from app.db import crud
from app.db.models import MoodLog
from langchain.llms import Groq
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