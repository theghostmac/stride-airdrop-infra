from typing import Dict

class SummaryGenerator:
    @staticmethod
    def generate_summary(delegations: Dict[str, Dict[str, int]], rewards: Dict[str, int]) -> Dict[str, int]:
        total_staked = sum(sum(user_delegations.values()) for user_delegations in delegations.values())
        largest_staked = max(sum(user_delegations.values()) for user_delegations in delegations.values())
        total_users = len(delegations)
        eligible_users = len(rewards)

        return {
            "total_staked_balance": total_staked,
            "largest_staked_balance": largest_staked,
            "total_users_with_balance": total_users,
            "total_eligible_users": eligible_users,
        }

if __name__ == "__main__":
    from calculator import RewardCalculator
    from scraper.storage_manager import StorageManager

    storage_manager = StorageManager("stride-airdrop-bucket")
    calculator = RewardCalculator(storage_manager)
    delegations, rewards = calculator.process_rewards()

    summary = SummaryGenerator.generate_summary(delegations, rewards)
    print("Daily Summary:")
    for key, value in summary.items():
        print(f"{key}: {value}")
