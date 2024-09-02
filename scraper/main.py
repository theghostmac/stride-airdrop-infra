import logging
from datetime import datetime
from delegation_scraper import process_all_delegations
from storage_manager import StorageManager
from database.db_manager import DatabaseManager
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize StorageManager
        storage = StorageManager("stride-airdrop-bucket")

        # Initialize DatabaseManager
        db_manager = DatabaseManager(os.environ.get('DATABASE_URL'))

        # Process all delegations
        logger.info("Processing all delegations...")
        user_delegations = process_all_delegations()
        logger.info(f"Processed delegations for {len(user_delegations)} users.")

        # Store delegations in S3
        today = datetime.utcnow().strftime("%Y-%m-%d")
        logger.info(f"Storing delegations in S3 for {today}...")
        storage.store_delegations(user_delegations, today)
        logger.info("Delegations stored successfully in S3.")

        # Store delegations in PostgreSQL
        logger.info(f"Storing delegations in PostgreSQL for {today}...")
        db_manager.store_stakes(user_delegations, datetime.utcnow())
        logger.info("Delegations stored successfully in PostgreSQL.")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()