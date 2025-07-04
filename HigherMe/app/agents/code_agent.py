import os
import httpx
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.db import crud
from app.tools.xp_calculator import calculateXp

load_dotenv()

WAKATIME_API_KEY = os.getenv("wakatime_api")
INSIGHTS_API_URL = "https://wakatime.com/api/v1/users/current/insights"

def get_git_stats():
    """Get git statistics for lines added/removed today"""
    try:
        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Run git log to get today's commits with stat information
        git_cmd = [
            'git', 'log', 
            '--since', today,
            '--until', f'{today} 23:59:59',
            '--pretty=format:',
            '--numstat'
        ]
        
        result = subprocess.run(git_cmd, capture_output=True, text=True, cwd=os.getcwd())
        
        if result.returncode != 0:
            print(f"⚠️ Git command failed: {result.stderr}")
            return {"lines_added": 0, "lines_removed": 0}
        
        lines_added = 0
        lines_removed = 0
        
        # Parse the numstat output
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
        print(f"⚠️ Error getting git stats: {e}")
        return {"lines_added": 0, "lines_removed": 0}

def get_coding_insights():
    """Fetch coding insights from WakaTime API"""
    headers = {
        "Authorization": f"Basic {WAKATIME_API_KEY}"
    }

    try:
        # Get daily average coding time for last 7 days
        daily_avg_url = f"{INSIGHTS_API_URL}/daily_average/last_7_days"
        response = httpx.get(daily_avg_url, headers=headers)
        response.raise_for_status()
        daily_avg_data = response.json()

        # Get languages used in last 7 days
        languages_url = f"{INSIGHTS_API_URL}/languages/last_7_days"
        lang_response = httpx.get(languages_url, headers=headers)
        lang_response.raise_for_status()
        languages_data = lang_response.json()

        # Extract daily average seconds and convert to minutes
        daily_avg_seconds = daily_avg_data["data"]["daily_average"]["total_seconds"]
        daily_avg_minutes = daily_avg_seconds / 60 if daily_avg_seconds else 0

        # Extract top languages
        top_languages = []
        if languages_data["data"]["languages"]:
            top_languages = [lang["name"] for lang in languages_data["data"]["languages"][:3]]

        return {
            "daily_avg_minutes": int(daily_avg_minutes),
            "top_languages": top_languages,
            "is_up_to_date": daily_avg_data["data"]["is_up_to_date"],
            "range": daily_avg_data["data"]["human_readable_range"]
        }

    except Exception as e:
        print(f"⚠️ Error fetching WakaTime insights: {e}")
        return {
            "daily_avg_minutes": 0,
            "top_languages": [],
            "is_up_to_date": False,
            "range": "unknown"
        }

def run_code_agent():
    """Run the code agent to track coding activity and award XP"""
    insights = get_coding_insights()
    git_stats = get_git_stats()

    metrics = {
        "lines_added": git_stats["lines_added"],
        "lines_removed": git_stats["lines_removed"],
        "total_time_minutes": insights["daily_avg_minutes"],
        "top_languages": insights["top_languages"]
    }

    # Log code stats
    crud.create_code_log(
        lines_Added=metrics["lines_added"],
        lines_Removed=metrics["lines_removed"],
        total_Time_Minutes=metrics["total_time_minutes"]
    )

    # Calculate XP
    xp_result = calculateXp(event_type="coding", metrics=metrics)
    crud.create_xp_event(xp_type="coding", amount=xp_result["xp"])
    crud.update_level(new_xp=xp_result["xp"])

    print(f"💻 CodeAgent XP Summary:")
    print(f"   Lines Added: {git_stats['lines_added']}")
    print(f"   Lines Removed: {git_stats['lines_removed']}")
    print(f"   Daily Average: {insights['daily_avg_minutes']} minutes")
    print(f"   Top Languages: {', '.join(insights['top_languages']) if insights['top_languages'] else 'None'}")
    print(f"   Data Range: {insights['range']}")
    print(f"   {xp_result['details']}")
    
    if not insights["is_up_to_date"]:
        print("   ⚠️ Note: WakaTime data may not be up to date")
