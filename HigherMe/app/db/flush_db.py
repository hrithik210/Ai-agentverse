import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.database import engine, Base
from app.db.models import CodeLog, HealthLog, MoodLog, XPEvent, Level

def flush_database():
    """
    Drops all tables from the database and recreates them.
    """
    print("⚠️ WARNING: This will delete all data in the database.")
    confirm = input("Are you sure you want to continue? (y/n): ")
    if confirm.lower() != 'y':
        print("Aborting.")
        return

    print("Dropping all tables...")
    try:
        Base.metadata.drop_all(bind=engine)
        print("✅ All tables dropped successfully.")
        
        print("Recreating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables recreated successfully.")
        
    except Exception as e:
        print(f"❌ Error flushing database: {e}")

if __name__ == "__main__":
    flush_database()
