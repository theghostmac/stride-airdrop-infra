from fastapi import APIRouter, Depends
from database.db_manager import DatabaseManager
from api.dependencies import get_db
from datetime import datetime, UTC

router = APIRouter()

@router.get("/summary")
def get_summary(db: DatabaseManager = Depends(get_db)):
    return db.get_average_summary()


@router.get("/summary/{date")
def get_daily_summary(date: str, db: DatabaseManager = Depends(get_db)):
    date_obj = datetime.strptime(date, "%Y-%m-%d").replace(tzinfo=UTC)
    summary = db.get_daily_summary(date_obj)

    if summary:
        return {
            "total_staked": summary.total_staked,
            "average_staked": summary.average_staked,
            "largest_staked": summary.largest_stake,
            "total_users": summary.total_users,
            "eligible_users": summary.eligible_users,
        }

    return {"error": "No summary found for the given date"}
