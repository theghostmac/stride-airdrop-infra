from fastapi import APIRouter, Depends
from database.db_manager import DatabaseManager
from api.dependencies import get_db

router = APIRouter()

@router.get("/rewards/{address}")
def get_rewards(address: str, db: DatabaseManager = Depends(get_db)):
    rewards = db.get_user_rewards(address)
    total_rewards = sum(reward.amount for reward in rewards)

    return {
        "address": address,
        "amount": total_rewards
    }
