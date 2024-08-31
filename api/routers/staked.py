from fastapi import APIRouter, Depends
from database.db_manager import DatabaseManager
from api.dependencies import get_db
from datetime import datetime, UTC

router = APIRouter()

@router.get("/staked/{address}")
def get_staked(address: str, date: str = None, db: DatabaseManager = Depends(get_db)):
    if date:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
    else:
        date_obj = datetime.now(UTC).date()

    stakes = db.get_user_stakes(address, date_obj)
    total_staked = sum(stake.amount for stake in stakes)

    return {
        "date": date_obj.strftime("%Y-%m-%d"),
        "address": address,
        "amount": total_staked
    }