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