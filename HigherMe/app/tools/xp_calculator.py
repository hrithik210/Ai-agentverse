def calculateXp(event_type : str , metrics : dict) -> dict :
  """
    Calculates XP based on event_type and input metrics.
    Returns a dict with XP amount and breakdown details.
    """
  xp = 0
  details = ""
  
  if event_type == 'coding':
    lines_added = metrics.get('lines_added' , 0)
    lines_removed = metrics.get("lines_removed" , 0)
    minutes_spent = metrics.get("total_time_minutes" , 0)
    
    xp += (lines_added + lines_removed) // 10    # 1 XP per 10 lines
    xp += minutes_spent // 10                          # 1 XP per 10 mins coding
    
    details = f"💻 Coding XP: +{xp} total ({(lines_added + lines_removed)} lines, {minutes_spent} mins)"
  
  elif event_type == "health":
        sleep = metrics.get("sleep_hours", 0)
        water = metrics.get("water_intake_liters", 0)
        exercise = metrics.get("exercise_minutes", 0)
        meal_score = metrics.get("meal_score", 0)
        xp += int((meal_score + 1) * 5)

        if sleep >= 7:
            xp += 20
            details += "🛌 +20 XP for good sleep. "
        if water >= 2:
            xp += 10
            details += "💧 +10 XP for hydration. "
        if exercise >= 30:
            xp += 15
            details += "🏃 +15 XP for exercise. "
        if meals >= 3:
            xp += 5
            details += "🍽️ +5 XP for balanced meals. "
            
  elif event_type == "mood":
        mood_score = metrics.get("sentiment_score", 0)
        xp += int((mood_score + 1) * 5)  # sentiment score: -1 to 1 → 0–10 XP
        details = f"🧠 Mood XP: {xp} based on sentiment."
        
  else:
    details =  "unknown event type"
    
  return (
    {
      "xp_amount": xp,
      "details": details.strip(),
    
    }
  )