from sqlalchemy.orm import Session
from datetime import datetime, date
from db.models import MoodLog
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize LLM for mood summarization
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
)

def mood_summary(user_id: int, target_date: date = None) -> str:
    """
    Generate a summary of mood entries for a specific date.
    If no date is provided, summarize today's entries.
    
    Args:
        user_id (int): The ID of the user
        target_date (date, optional): The date to summarize. Defaults to today.
    
    Returns:
        str: A summary of the mood entries for the specified date
    """
    from db.database import get_db_session
    
    if target_date is None:
        target_date = datetime.now().date()
    
    db = get_db_session()
    try:
        # Get all mood logs for the user on the specified date
        mood_logs = db.query(MoodLog).filter(
            MoodLog.user_id == user_id,
            MoodLog.timestamp >= datetime.combine(target_date, datetime.min.time()),
            MoodLog.timestamp < datetime.combine(target_date, datetime.max.time())
        ).all()
        
        if not mood_logs:
            return "No mood entries recorded for this date."
        
        # Extract mood texts
        mood_texts = [log.mood_text for log in mood_logs]
        
        # Create a prompt for the LLM to summarize the mood entries
        prompt = f"""
You are a friendly, witty, and empathetic companion who understands human emotions deeply. Based on the following mood journal entries from a single day, write a concise 2-3 sentence summary that captures the emotional journey of the day in a warm, relatable way.

Instructions:
- Be silly, witty, empathic, and considerate
- Use casual, friendly language that a close friend might use
- Focus on the human experience and emotional patterns
- Avoid technical terms like "sentiment" or "emotional stimuli"
- Keep it brief and readable

Mood Entries:
{chr(10).join(f'- "{text}"' for text in mood_texts if text)}

Summary:"""
        
        # Generate summary using LLM
        try:
            response = llm.invoke(prompt)
            summary = response.content.strip()
            if summary:
                return summary
            else:
                # Fallback to simple summary if LLM returns empty response
                if len(mood_texts) == 1:
                    return f"Aha! You shared that you're feeling \"{mood_texts[0][:30]}...\" today - thanks for letting me know!"
                else:
                    return f"You shared {len(mood_logs)} mood updates today - that's awesome! Some of them were: {', '.join(mood_texts[:3])}..."
        except Exception as e:
            print(f"Error generating mood summary: {e}")
            # Fallback to simple summary
            if len(mood_texts) == 1:
                return f"Aha! You shared that you're feeling \"{mood_texts[0][:30]}...\" today - thanks for letting me know!"
            else:
                return f"You shared {len(mood_logs)} mood updates today - that's awesome! Some of them were: {', '.join(mood_texts[:3])}..."
    
    except Exception as e:
        print(f"Error retrieving mood logs: {e}")
        return "Unable to retrieve mood entries for summary."
    finally:
        db.close()

def mood_summary_with_sentiment(user_id: int, target_date: date = None) -> dict:
    """
    Generate a summary of mood entries with sentiment analysis for a specific date.
    
    Args:
        user_id (int): The ID of the user
        target_date (date, optional): The date to summarize. Defaults to today.
    
    Returns:
        dict: A dictionary containing the summary and sentiment statistics
    """
    from db.database import get_db_session
    
    if target_date is None:
        target_date = datetime.now().date()
    
    db = get_db_session()
    try:
        # Get all mood logs for the user on the specified date
        mood_logs = db.query(MoodLog).filter(
            MoodLog.user_id == user_id,
            MoodLog.timestamp >= datetime.combine(target_date, datetime.min.time()),
            MoodLog.timestamp < datetime.combine(target_date, datetime.max.time())
        ).all()
        
        if not mood_logs:
            return {
                "summary": "No mood entries recorded for this date.",
                "total_entries": 0,
                "average_sentiment": 0.0,
                "sentiment_trend": "neutral"
            }
        
        # Calculate sentiment statistics
        sentiments = [log.sentiment for log in mood_logs if log.sentiment is not None]
        if sentiments:
            avg_sentiment = sum(sentiments) / len(sentiments)
            if avg_sentiment > 0.3:
                trend = "positive"
            elif avg_sentiment < -0.3:
                trend = "negative"
            else:
                trend = "neutral"
        else:
            avg_sentiment = 0.0
            trend = "neutral"
        
        # Extract mood texts
        mood_texts = [log.mood_text for log in mood_logs]
        
        # Create a prompt for the LLM to summarize the mood entries
        # Include sentiment information when available, but don't filter out entries without sentiment
        mood_entries = []
        for text, log in zip(mood_texts, mood_logs):
            if text:  # Only include entries with actual text
                if log.sentiment is not None:
                    mood_entries.append(f'- "{text}" (sentiment: {log.sentiment:.2f})')
                else:
                    mood_entries.append(f'- "{text}"')
        
        prompt = f"""
You are a friendly, witty, and empathetic companion who understands human emotions deeply. Based on the following mood journal entries from a single day, write a concise 2-3 sentence summary that captures the emotional journey of the day in a warm, relatable way.

Instructions:
- Be silly, witty, empathic, and considerate
- Use casual, friendly language that a close friend might use
- Focus on the human experience and emotional patterns
- Avoid technical terms like "sentiment" or "emotional stimuli"
- Keep it brief and readable

Mood Entries:
{chr(10).join(mood_entries)}

Summary:"""
        
        # Generate summary using LLM
        try:
            response = llm.invoke(prompt)
            summary = response.content.strip()
            if summary:
                summary_text = summary
            else:
                # Fallback to simple summary if LLM returns empty response
                if len(mood_texts) == 1:
                    summary_text = f"Aha! You shared that you're feeling \"{mood_texts[0][:30]}...\" today - thanks for letting me know!"
                else:
                    summary_text = f"You shared {len(mood_logs)} mood updates today - that's awesome!"
        except Exception as e:
            print(f"Error generating mood summary: {e}")
            # Fallback to simple summary
            if len(mood_texts) == 1:
                summary_text = f"Aha! You shared that you're feeling \"{mood_texts[0][:30]}...\" today - thanks for letting me know!"
            else:
                summary_text = f"You shared {len(mood_logs)} mood updates today - that's awesome!"
        
        return {
            "summary": summary_text,
            "total_entries": len(mood_logs),
            "average_sentiment": round(avg_sentiment, 2),
            "sentiment_trend": trend
        }
    
    except Exception as e:
        print(f"Error retrieving mood logs: {e}")
        return {
            "summary": "Unable to retrieve mood entries for summary.",
            "total_entries": 0,
            "average_sentiment": 0.0,
            "sentiment_trend": "neutral"
        }
    finally:
        db.close()
