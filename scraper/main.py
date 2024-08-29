import logging
from datetime import datetime
from delegation_scraper import process_all_delegations
from storage_manager import StorageManager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        # Initialize StorageManager
        storage = StorageManager("stride-airdrop-bucket")

        # Process all delegations
        logger.info("Processing all delegations...")
        user_delegations = process_all_delegations()
        logger.info(f"Processed delegations for {len(user_delegations)} users.")

        # Store delegations
        today = datetime.utcnow().strftime("%Y-%m-%d")
        logger.info(f"Storing delegations for {today}...")
        storage.store_delegations(user_delegations, today)
        logger.info("Delegations stored successfully.")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()