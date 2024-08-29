from scraper.storage_manager import StorageManager
from calculator import RewardCalculator
from summary_generator import SummaryGenerator
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    try:
        storage_manager = StorageManager("stride-airdrop-bucket")
        calculator = RewardCalculator(storage_manager)

        date = datetime.utcnow().strftime("%Y-%m-%d")
        delegations, rewards = calculator.process_rewards(date)

        summary = SummaryGenerator.generate_summary(delegations, rewards)

        logger.info(f"Processed rewards for {len(rewards)} users")
        logger.info(f"Daily Summary: {summary}")

        # TODO: Store rewards and summary in the db. coming soon.

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()