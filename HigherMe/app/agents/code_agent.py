import os
import httpx
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.db import crud
from app.tools.xp_calculator import calculateXp

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
        
        # Debug: print raw output
        print(f"🔍 Git output for {today}:")
        print(f"Raw output: '{result.stdout}'")
        
        # Parse the numstat output
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('\t')
                print(f"   Parsing line: {parts}")
                if len(parts) >= 2:
                    # Handle cases where files are binary or renamed (shown as '-')
                    if parts[0].isdigit() and parts[1].isdigit():
                        lines_added += int(parts[0])
                        lines_removed += int(parts[1])
        
        print(f"   Found: +{lines_added} -{lines_removed}")
        
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
        
        print(f"🔍 Checking recent commits:")
        
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                parts = line.split('\t')
                if len(parts) >= 2 and parts[0].isdigit() and parts[1].isdigit():
                    lines_added += int(parts[0])
                    lines_removed += int(parts[1])
        
        print(f"   Recent commits: +{lines_added} -{lines_removed}")
        
        return {
            "lines_added": lines_added,
            "lines_removed": lines_removed
        }
        
    except Exception as e:
        print(f"⚠️ Error getting recent commit stats: {e}")
        return {"lines_added": 0, "lines_removed": 0}

def get_coding_summaries():
    """Fetch coding summaries from WakaTime API (free tier)"""
    headers = {
        "Authorization": f"Basic {WAKATIME_API_KEY}"
    }

    try:
        # Get today's coding summary
        today = datetime.now().strftime('%Y-%m-%d')
        params = {
            "start": today,
            "end": today
        }
        
        response = httpx.get(SUMMARIES_API_URL, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if not data["data"]:
            return {
                "total_minutes": 0,
                "top_languages": [],
                "is_up_to_date": True,
                "range": "today"
            }

        summary = data["data"][0]
        
        # Extract total minutes
        total_seconds = summary["grand_total"]["total_seconds"]
        total_minutes = total_seconds / 60 if total_seconds else 0

        # Extract top languages
        top_languages = []
        if summary.get("languages"):
            top_languages = [lang["name"] for lang in summary["languages"][:3]]

        return {
            "total_minutes": int(total_minutes),
            "top_languages": top_languages,
            "is_up_to_date": True,
            "range": f"today ({today})"
        }

    except Exception as e:
        print(f"⚠️ Error fetching WakaTime summaries: {e}")
        return {
            "total_minutes": 0,
            "top_languages": [],
            "is_up_to_date": False,
            "range": "unknown"
        }

def run_code_agent():
    """Run the code agent to track coding activity and award XP"""
    summaries = get_coding_summaries()
    git_stats = get_git_stats()

    metrics = {
        "lines_added": git_stats["lines_added"],
        "lines_removed": git_stats["lines_removed"],
        "total_time_minutes": summaries["total_minutes"],
        "top_languages": summaries["top_languages"]
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
    print(f"   Total Time Today: {summaries['total_minutes']} minutes")
    print(f"   Top Languages: {', '.join(summaries['top_languages']) if summaries['top_languages'] else 'None'}")
    print(f"   Data Range: {summaries['range']}")
    print(f"   {xp_result['details']}")
    
    if not summaries["is_up_to_date"]:
        print("   ⚠️ Note: WakaTime data may not be up to date")
