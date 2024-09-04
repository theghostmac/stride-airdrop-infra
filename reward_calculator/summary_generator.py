from typing import Dict
from .claim_tracker import ClaimTracker

class SummaryGenerator:
    @staticmethod
    def generate_summary(delegations: Dict[str, Dict[str, int]], rewards: Dict[str, int], claim_tracker: ClaimTracker, date: str) -> Dict[str, int]:
        total_staked = sum(sum(user_delegations.values()) for user_delegations in delegations.values())
        largest_staked = max(sum(user_delegations.values()) for user_delegations in delegations.values())
        total_users = len(delegations)
        eligible_users = len(rewards)
        early_claimers = claim_tracker.get_early_claimers_count(date)

        return {
            "total_staked_balance": total_staked,
            "largest_staked_balance": largest_staked,
            "total_users_with_balance": total_users,
            "total_eligible_users": eligible_users,
            "early_claimers": early_claimers,
        }

if __name__ == "__main__":
    from calculator import RewardCalculator
    from scraper.storage_manager import StorageManager
    from datetime import datetime

    storage_manager = StorageManager("stride-airdrop-bucket")
    calculator = RewardCalculator(storage_manager)
    date = datetime.utcnow().strftime("%Y-%m-%d")
    delegations, rewards = calculator.process_rewards()

    summary = SummaryGenerator.generate_summary(delegations, rewards, calculator.claim_tracker, date)
    print("Daily Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")
