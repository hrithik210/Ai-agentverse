from app.agents.daily_report_agent import build_daily_report
from app.db.database import get_db

def test():
    db = get_db()
    if db:
        report = build_daily_report(db)
        print(report)

if __name__ == "__main__":
    test()