from fastapi import APIRouter, Depends
from database.db_manager import DatabaseManager
from api.dependencies import get_db

router = APIRouter()

@router.post("/claim/{address}")
def claim_rewards(address: str, db: DatabaseManager = Depends(get_db)):
    claimed_amount = db.claim_rewards(address)

    return {"address": address, "claimed_amount": claimed_amount}