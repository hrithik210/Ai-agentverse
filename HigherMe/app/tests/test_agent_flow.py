import sys
import os
from datetime import datetime
import time
import logging
from app.agents.mood_agent import log_mood
from app.agents.health_agent import  log_meal, log_water_intake, log_sleep, log_exercise
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
            # Log another mood entry later in the day
            time.sleep(1)  # Small delay to ensure different timestamps
            log_mood("Feeling accomplished after finishing my tasks!")
        except Exception as e:
            logger.error(f"Error logging mood: {e}")
        
        # Step 2: Log health activities throughout the day
        logger.info("💪 Testing health logging with multiple entries...")
        try:
            # Morning activities
            logger.info("🌅 Morning health logs...")
            log_sleep(8.0)  # Log sleep from previous night
            log_meal("Breakfast: Oatmeal with berries and honey")
            log_water_intake(0.5)  # Morning water
            
            # Midday activities
            time.sleep(1)  # Small delay to simulate time passing
            logger.info("🌞 Midday health logs...")
            log_meal("Lunch: Grilled chicken salad with olive oil dressing")
            log_water_intake(0.75)  # Midday water
            log_exercise(45)  # Midday workout
            
            # Evening activities
            time.sleep(1)  # Small delay to simulate time passing
            logger.info("🌙 Evening health logs...")
            log_meal("Dinner: Salmon with steamed vegetables and quinoa")
            log_water_intake(1.0)  # Evening water
            
            
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
        
        # Check mood logs
        mood_logs = db.query(MoodLog).filter(
            MoodLog.timestamp >= today,
            MoodLog.processed == processed
        ).all()
        logger.info(f"Found {len(mood_logs)} {'processed' if processed else 'unprocessed'} mood logs")
        for i, log in enumerate(mood_logs):
            logger.info(f"  Mood {i+1}: {log.mood_text[:30]}... (Sentiment: {log.sentiment:.2f})")
        
        # Check health logs with more detail
        health_logs = db.query(HealthLog).filter(
            HealthLog.date >= today,
            HealthLog.processed == processed
        ).order_by(HealthLog.date).all()
        logger.info(f"Found {len(health_logs)} {'processed' if processed else 'unprocessed'} health logs")
        
        # If there are multiple health logs, show the progression
        if len(health_logs) > 0:
            logger.info("Health log details:")
            for i, log in enumerate(health_logs):
                logger.info(f"  Log {i+1} @ {log.date.strftime('%H:%M:%S')}:")
                logger.info(f"    Meals: {log.meals[:50]}...")
                logger.info(f"    Sleep: {log.sleep_hours} hours")
                logger.info(f"    Water: {log.water_intake_liter} liters")
                logger.info(f"    Exercise: {log.exercise_minutes} minutes")
            
            # Show the final accumulated values
            latest_log = health_logs[-1]
            logger.info("Final accumulated health values:")
            logger.info(f"  Sleep: {latest_log.sleep_hours} hours")
            logger.info(f"  Total Water: {latest_log.water_intake_liter} liters")
            logger.info(f"  Exercise: {latest_log.exercise_minutes} minutes")
            logger.info(f"  All Meals: {latest_log.meals}")
        
        # Check code logs
        code_logs = db.query(CodeLog).filter(
            CodeLog.date >= today,
            CodeLog.processed == processed
        ).all()
        logger.info(f"Found {len(code_logs)} {'processed' if processed else 'unprocessed'} code logs")
        for i, log in enumerate(code_logs):
            logger.info(f"  Code Log {i+1}: +{log.lines_added} lines, -{log.lines_removed} lines, {log.total_time_minutes} mins")
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

def test_health_multiple_logs():
    """
    Test specifically the health agent's ability to handle multiple logs throughout the day
    """
    logger.info("🚀 Starting health multiple logs test...")
    
    try:
        # Clear any existing logs for today (for clean test)
        db = get_db_session()
        today = datetime.now().date()
        try:
            db.query(HealthLog).filter(HealthLog.date >= today).delete()
            db.query(XPEvent).filter(XPEvent.timestamp >= today, XPEvent.xp_type == "health").delete()
            db.commit()
        except Exception as e:
            logger.error(f"Error clearing existing logs: {e}")
            db.rollback()
        finally:
            db.close()
        
        # Morning routine
        logger.info("🌅 Morning health logs...")
        log_sleep(7.5)  # Log sleep hours
        log_meal("Breakfast: Eggs and toast")
        log_water_intake(0.5)  # 500ml in the morning
        
        # Verify first set of logs
        logger.info("Checking health logs after morning entries...")
        verify_logged_data(processed=False)
        
        # Lunchtime
        logger.info("🍲 Lunchtime health logs...")
        log_meal("Lunch: Chicken sandwich with salad")
        log_water_intake(0.75)  # Another 750ml
        
        # Verify after lunch
        logger.info("Checking health logs after lunch entries...")
        verify_logged_data(processed=False)
        
        # Afternoon
        logger.info("🏋️ Afternoon health logs...")
        log_exercise(30)  # 30 min workout
        log_water_intake(0.5)  # Post-workout hydration
        
        # Evening
        logger.info("🌙 Evening health logs...")
        log_meal("Dinner: Pasta with vegetables")
        log_water_intake(0.5)  # Evening water
        
        # Final verification before processing
        logger.info("Final verification before processing...")
        verify_logged_data(processed=False)
        
        # Run the health agent to process logs
        from app.agents.health_agent import run_health_agent
        logger.info("⏰ Running health agent...")
        run_health_agent()
        
        # Verify processed data and XP awards
        logger.info("🔍 Verifying processed data...")
        verify_logged_data(processed=True)
        verify_xp_awards()
        
        logger.info("✨ Health multiple logs test complete!")
        
    except Exception as e:
        logger.error(f"❌ Error during test: {e}")
        raise

if __name__ == "__main__":
    try:
        # Choose which test to run
        test_complete_flow()
        # Uncomment to run the health-specific test
        # test_health_multiple_logs()
    except Exception as e:
        logger.error(f"Test failed: {e}")
        sys.exit(1)
