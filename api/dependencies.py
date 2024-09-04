from database.db_manager import DatabaseManager
from functools import lru_cache
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

@lru_cache()
def get_db_manager():
    return DatabaseManager(DATABASE_URL)

def get_db():
    db = get_db_manager()
    try:
        yield db
    finally:
        pass