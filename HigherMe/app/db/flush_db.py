import sys
import os

# Add the project root to the Python path to allow for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from app.db.database import engine, Base
from app.db.models import User, CodeLog, HealthLog, MoodLog, XPEvent, Level
from sqlalchemy import text

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
        # First try the normal drop
        try:
            Base.metadata.drop_all(bind=engine)
            print("✅ All tables dropped successfully.")
        except Exception as e:
            print(f"⚠️ Normal drop failed: {e}")
            print("🔄 Attempting CASCADE drop for orphaned tables...")
            
            # Use raw SQL to drop all tables with CASCADE
            with engine.connect() as conn:
                # Get all table names
                result = conn.execute(text("""
                    SELECT tablename FROM pg_tables 
                    WHERE schemaname = 'public'
                """))
                tables = [row[0] for row in result]
                
                print(f"Found tables: {tables}")
                
                # Drop each table with CASCADE
                for table in tables:
                    try:
                        conn.execute(text(f"DROP TABLE IF EXISTS {table} CASCADE"))
                        print(f"✅ Dropped table: {table}")
                    except Exception as table_error:
                        print(f"⚠️ Could not drop {table}: {table_error}")
                
                conn.commit()
            
            print("✅ All tables dropped with CASCADE.")
        
        print("Recreating all tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables recreated successfully.")
        
    except Exception as e:
        print(f"❌ Error flushing database: {e}")

if __name__ == "__main__":
    flush_database()
