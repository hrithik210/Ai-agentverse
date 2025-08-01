from sqlalchemy.orm import Session
from datetime import datetime, date
from db.models import HealthLog
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

# Initialize LLM for health summarization
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.0,
    max_retries=2,
)

def health_summary(user_id: int, target_date: date = None) -> str:
    """
    Generate a summary of health entries for a specific date.
    If no date is provided, summarize today's entries.
    
    Args:
        user_id (int): The ID of the user
        target_date (date, optional): The date to summarize. Defaults to today.
    
    Returns:
        str: A summary of the health entries for the specified date
    """
    from db.database import get_db_session
    
    if target_date is None:
        target_date = datetime.now().date()
    
    db = get_db_session()
    try:
        # Get all health logs for the user on the specified date
        health_logs = db.query(HealthLog).filter(
            HealthLog.user_id == user_id,
            HealthLog.date >= datetime.combine(target_date, datetime.min.time()),
            HealthLog.date < datetime.combine(target_date, datetime.max.time())
        ).all()
        
        if not health_logs:
            return "No health entries recorded for this date."
        
        # Extract health log details and format them as text strings
        health_entries = []
        for log in health_logs:
            entry_parts = []
            if log.meals and log.meals.strip():
                entry_parts.append(f"meal: {log.meals}")
            if log.sleep_hours and log.sleep_hours > 0:
                entry_parts.append(f"sleep: {log.sleep_hours} hours")
            if log.exercise_minutes and log.exercise_minutes > 0:
                entry_parts.append(f"exercise: {log.exercise_minutes} minutes")
            if log.water_intake_liter and log.water_intake_liter > 0:
                entry_parts.append(f"water: {log.water_intake_liter} liters")
            
            if entry_parts:
                health_entries.append(", ".join(entry_parts))
        
        if not health_entries:
            # Fallback if no meaningful health data
            if len(health_logs) == 1:
                return "Nice work taking care of yourself today!"
            else:
                return f"You focused on your health {len(health_logs)} times today - that's awesome!"
        
        # Create a prompt for the LLM to summarize the health entries
        prompt = f"""
You are a friendly, witty, and empathetic health companion who understands that health journeys are personal and unique. Based on the following health activities from a single day, write a concise 2-3 sentence summary that captures the health journey of the day in a warm, relatable way.

Instructions:
- Be silly, witty, empathic, and considerate
- Use casual, friendly language that a supportive friend might use
- Acknowledge effort and progress, no matter how small
- Celebrate wins and gently encourage continued growth
- Avoid technical terms and keep it relatable

Health Activities:
{chr(10).join(f'- {entry}' for entry in health_entries if entry)}

Summary:"""
        
        # Generate summary using LLM
        try:
            response = llm.invoke(prompt)
            summary = response.content.strip()
            if summary:
                return summary
            else:
                # Fallback to simple summary if LLM returns empty response
                if len(health_entries) == 1:
                    return "Nice work taking care of yourself today!"
                else:
                    return f"You focused on your health {len(health_logs)} times today - that's awesome!"
        except Exception as e:
            print(f"Error generating health summary: {e}")
            # Fallback to simple summary
            if len(health_entries) == 1:
                return "Nice work taking care of yourself today!"
            else:
                return f"You focused on your health {len(health_logs)} times today - that's awesome!"
    
    except Exception as e:
        print(f"Error retrieving health logs: {e}")
        return "Unable to retrieve health entries for summary."
    finally:
        db.close()
