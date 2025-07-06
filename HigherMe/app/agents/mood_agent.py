from db.database import get_db
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
    sentiment_score = float(response.strip())
    return sentiment_score
  
  except Exception as e:
    print(f"Error analyzing mood sentiment: {e}")
    return 0.0
  

def run_mood_agent(mood_text: str, db: Session):
    sentiment_score = analyze_mood_sentiment(mood_text)

    # Log mood entry — no XP here
    crud.create_mood_log(
        db=db,
        mood_text=mood_text,
        sentiment=sentiment_score
    )

    print(f"✅ Mood logged with sentiment score: {sentiment_score}")