from app.agents.daily_report_agent import build_daily_report
from app.db.database import get_db_session

def test():
    db = get_db_session()
    if db:
        try:
            report = build_daily_report(db)
            print(report)
        finally:
            db.close()

if __name__ == "__main__":
    test()