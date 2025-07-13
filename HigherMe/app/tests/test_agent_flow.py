import sys
import os
from datetime import datetime
import time
import logging
from app.agents.mood_agent import log_mood
from app.agents.health_agent import log_health_activity
from app.agents.code_agent import log_code_activity
from app.scheduler.scheduler import run_all_daily_tasks
from app.db.database import get_db_session
from app.db.models import MoodLog, HealthLog, CodeLog, XPEvent, Level

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_complete_flow():
    """
    Test the complete flow of logging activities and processing them via scheduler
    """
    logger.info("🚀 Starting complete flow test...")
    
    try:
        # Step 1: Log a mood entry
        logger.info("🎭 Testing mood logging...")
        try:
            log_mood("I'm feeling very productive and happy today!")
        except Exception as e:
            logger.error(f"Error logging mood: {e}")
        
        # Step 2: Log health activities
        logger.info("💪 Testing health logging...")
        try:
            log_health_activity(
                meals="Oatmeal for breakfast, Salad for lunch",
                sleep_hours=8.0,
                water_liters=2.5,
                exercise_minutes=45
            )
        except Exception as e:
            logger.error(f"Error logging health activity: {e}")
        
        # Step 3: Log some code activity
        logger.info("💻 Testing code logging...")
        try:
            log_code_activity()
        except Exception as e:
            logger.error(f"Error logging code activity: {e}")
        
        # Step 4: Verify logged data
        logger.info("✅ Verifying logged data...")
        verify_logged_data(processed=False)
        
        # Step 5: Run scheduler tasks (simulating end-of-day)
        logger.info("⏰ Running scheduler tasks...")
        run_all_daily_tasks()
        
        # Step 6: Verify processed data and XP awards
        logger.info("🔍 Verifying processed data and XP awards...")
        verify_processed_data()
        verify_xp_awards()
        
        logger.info("✨ Test complete!")
        
    except Exception as e:
        logger.error(f"❌ Error during test: {e}")
        raise

def verify_logged_data(processed=False):
    """Verify that data was logged correctly"""
    db = get_db_session()
    try:
        today = datetime.now().date()
        
        mood_logs = db.query(MoodLog).filter(
            MoodLog.timestamp >= today,
            MoodLog.processed == processed
        ).all()
        logger.info(f"Found {len(mood_logs)} {'processed' if processed else 'unprocessed'} mood logs")
        
        health_logs = db.query(HealthLog).filter(
            HealthLog.date >= today,
            HealthLog.processed == processed
        ).all()
        logger.info(f"Found {len(health_logs)} {'processed' if processed else 'unprocessed'} health logs")
        
        code_logs = db.query(CodeLog).filter(
            CodeLog.date >= today,
            CodeLog.processed == processed
        ).all()
        logger.info(f"Found {len(code_logs)} {'processed' if processed else 'unprocessed'} code logs")
    except Exception as e:
        logger.error(f"Error verifying logged data: {e}")
    finally:
        db.close()

def verify_processed_data():
    """Verify that data was processed by the scheduler"""
    verify_logged_data(processed=True)

def verify_xp_awards():
    """Verify that XP was awarded correctly"""
    db = get_db_session()
    try:
        today = datetime.now().date()
        
        xp_events = db.query(XPEvent).filter(
            XPEvent.timestamp >= today
        ).all()
        
        logger.info("🏆 XP Awards for today:")
        for event in xp_events:
            logger.info(f"- {event.xp_type}: +{event.amount} XP")
        
        level = db.query(Level).first()
        if level:
            logger.info(f"Current Level: {level.current_level}, Total XP: {level.total_xp}")
    except Exception as e:
        logger.error(f"Error verifying XP awards: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    try:
        test_complete_flow()
    except Exception as e:
        logger.error(f"Test failed: {e}")
        sys.exit(1)
