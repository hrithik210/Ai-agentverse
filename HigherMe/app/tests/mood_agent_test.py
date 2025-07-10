
from app.agents.mood_agent import run_mood_agent, calculate_daily_mood_xp

def test():
    print("🌤️ Testing MoodAgent with multiple entries...")
    
    # Log multiple mood entries
    run_mood_agent("Woke up feeling meh, dragged through the morning.")
    run_mood_agent("Got into flow around lunch, banged out some code.")
    run_mood_agent("Had a nice walk, feeling calm and clear-headed.")
    
    # Simulate end-of-day XP calculation
    print("\n⏰ Simulating end-of-day XP calculation...")
    calculate_daily_mood_xp()
    
    print("\n✅ Test complete.")

if __name__ == "__main__":
    test()