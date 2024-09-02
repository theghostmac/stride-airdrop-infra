from database.db_manager import DatabaseManager
from scraper.storage_manager import StorageManager
from calculator import RewardCalculator
from summary_generator import SummaryGenerator
from datetime import datetime
import os
from datetime import datetime, UTC

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        storage_manager = StorageManager("stride-airdrop-bucket")
        calculator = RewardCalculator(storage_manager)

        date = datetime.now(UTC)
        date_str = date.strftime("%Y-%m-%d")

        delegations, rewards = calculator.process_rewards(date_str)

        summary = SummaryGenerator.generate_summary(delegations, rewards)

        logger.info(f"Processed rewards for {len(rewards)} users")
        logger.info(f"Daily Summary: {summary}")

        # Store rewards and summary in the database
        db_manager = DatabaseManager(os.getenv('DATABASE_URL'))
        db_manager.store_rewards(rewards, date)
        db_manager.store_daily_summary(summary, date)

        # simulating claims for testing
        for address in list(rewards.keys())[:10]:
            claimed_reward = calculator.claim_reward(address, date_str)
            logger.info(f"Address {address} claimed {claimed_reward} ustrd")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()