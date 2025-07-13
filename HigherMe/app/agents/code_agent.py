import os
import httpx
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.db import crud
from app.tools.xp_calculator import calculateXp
from app.db.database import get_db_session
from app.db.models import CodeLog, XPEvent

load_dotenv()

WAKATIME_API_KEY = os.getenv("wakatime_api")
SUMMARIES_API_URL = "https://wakatime.com/api/v1/users/current/summaries"

def get_git_stats():
    """Get git statistics for lines added/removed today"""
    try:
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime('%Y-%m-%d')
        
        # First, let's try a simpler approach - get all commits from today
        git_cmd = [
            'git', 'log', 
            '--since', f'{today} 00:00:00',
            '--until', f'{today} 23:59:59',
            '--pretty=format:',
            '--numstat'
        ]
        
        result = subprocess.run(git_cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode != 0:
            print(f"⚠️ Git command failed: {result.stderr}")
            # Try alternative approach - get stats from last few commits
            return get_recent_commit_stats()
        
        lines_added = 0
        lines_removed = 0
        
        # Parse the numstat output
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2:
                    # Handle cases where files are binary or renamed (shown as '-')
                    if parts[0].isdigit() and parts[1].isdigit():
                        lines_added += int(parts[0])
                        lines_removed += int(parts[1])
        
        return {
            "lines_added": lines_added,
            "lines_removed": lines_removed
        }
        
    except Exception as e:
        print(f"⚠️ Error getting git stats: {e}")
        return {"lines_added": 0, "lines_removed": 0}

def get_recent_commit_stats():
    """Alternative method: get stats from recent commits (last 5)"""
    try:
        git_cmd = [
            'git', 'log', 
            '-5',  # Last 5 commits
            '--pretty=format:',
            '--numstat'
        ]
        
        result = subprocess.run(git_cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode != 0:
            return {"lines_added": 0, "lines_removed": 0}
        
        lines_added = 0
        lines_removed = 0
        
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                    lines_added += int(parts[0])
                    lines_removed += int(parts[1])
        
        return {
            "lines_added": lines_added,
            "lines_removed": lines_removed
        }
        
    except Exception as e:
        print(f"⚠️ Error getting recent commit stats: {e}")
        return {"lines_added": 0, "lines_removed": 0}

def log_code_activity():
    """
    Log code activity without calculating XP.
    XP will be calculated by the scheduler at the end of the day.
    """
    db_session = get_db_session()
    try:
        # Get git stats
        git_stats = get_git_stats()
        
        # Calculate total time from WakaTime if available
        total_time_minutes = 0
        if WAKATIME_API_KEY:
            # Add WakaTime integration here if needed
            pass
        
        # Store code activity
        code_log = crud.create_code_log(
            db=db_session,
            lines_added=git_stats["lines_added"],
            lines_removed=git_stats["lines_removed"],
            total_time_minutes=total_time_minutes
        )
        
        print(f"✅ Code activity logged: +{git_stats['lines_added']}/-{git_stats['lines_removed']} lines")
        print("📊 Code XP will be calculated at the end of the day")
        return code_log
        
    except Exception as e:
        print(f"❌ Error logging code activity: {e}")
    finally:
        db_session.close()

def run_code_agent():
    """
    Calculate XP for all unprocessed code logs.
    This function is called by the scheduler.
    """
    db_session = get_db_session()
    try:
        today = datetime.now().date()
        
        # Check if XP has already been awarded for code today
        xp_awarded = db_session.query(XPEvent).filter(
            XPEvent.timestamp >= today,
            XPEvent.xp_type == "code"
        ).first()
        
        if xp_awarded:
            print(f"⚠️ Code XP already awarded today ({xp_awarded.amount} XP). Skipping.")
            return
        
        # Get unprocessed code logs from today
        code_logs = db_session.query(CodeLog).filter(
            CodeLog.date >= today,
            CodeLog.processed == False
        ).order_by(CodeLog.date).all()
        
        if not code_logs:
            print("ℹ️ No unprocessed code logs found for today. No XP awarded.")
            return
        
        # Calculate total metrics for the day
        total_lines_added = sum(log.lines_added for log in code_logs)
        total_lines_removed = sum(log.lines_removed for log in code_logs)
        total_time = sum(log.total_time_minutes for log in code_logs)
        
        # Calculate XP once for all activity
        metrics = {
            "lines_added": total_lines_added,
            "lines_removed": total_lines_removed,
            "total_time_minutes": total_time
        }
        
        xp_result = calculateXp(event_type="code", metrics=metrics)
        
        # Award XP
        crud.award_daily_xp("code", xp_result["xp"])
        
        # Mark all logs as processed
        now = datetime.now()
        for log in code_logs:
            log.processed = True
            log.processed_at = now
        
        db_session.commit()
        
        print(f"🧠 Daily Code XP Awarded: +{xp_result['xp']} XP")
        if 'details' in xp_result:
            print(f"📝 {xp_result['details']}")
            
    except Exception as e:
        print(f"❌ Error calculating code XP: {e}")
        db_session.rollback()
    finally:
        db_session.close()
