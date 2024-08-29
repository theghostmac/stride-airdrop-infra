from typing import Dict, List, Tuple
from scraper.storage_manager import StorageManager
from datetime import datetime, timedelta


class RewardCalculator:
    def __init__(self, storage_manager: StorageManager):
        self.storage_manager = storage_manager
        self.total_daily_reward = 1_000_000 * 1_000_000  # 1M STRD in ustrd is the fixed reward to stakers, daily.

    def get_delegations(self, date: str = None) -> Dict[str, Dict[str, int]]:
        if date is None:
            date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        return self.storage_manager.retrieve_delegations(date)

    def calculate_rewards(self, delegations: Dict[str, Dict[str, int]]) -> Dict[str, int]:
        total_staked = sum(sum(user_delegations.values()) for user_delegations in delegations.values())
        # anyone who stakes over 1 STRD (1000000ustrd) is eligible.
        eligible_users = {user: sum(stakes.values()) for user, stakes in delegations.items() if
                          sum(stakes.values()) >= 1_000_000}

        if not eligible_users:
            return {}

        sorted_users = sorted(eligible_users.items(), key=lambda x: x[1], reverse=True)
        top_1_percent = max(1, int(len(sorted_users) * 0.01))
        top_5_percent = max(1, int(len(sorted_users) * 0.05))

        rewards = {}
        # there is a 2x multiplier for the stakers in top 1% a 1.5x in top 5%.
        for i, (user, stake) in enumerate(sorted_users):
            base_reward = (stake / total_staked) * self.total_daily_reward
            if i < top_1_percent:
                multiplier = 2
            elif i < top_5_percent:
                multiplier = 1.5
            else:
                multiplier = 1
            rewards[user] = int(base_reward * multiplier)

        return rewards

    def process_rewards(self, date: str = None) -> tuple[dict[str, dict[str, int]], dict[str, int]]:
        delegations = self.get_delegations(date)
        rewards = self.calculate_rewards(delegations)
        return delegations, rewards


if __name__ == "__main__":
    storage_manager = StorageManager("stride-airdrop-bucket")
    calculator = RewardCalculator(storage_manager)
    delegations, rewards = calculator.process_rewards()
    print(f"Processed rewards for {len(rewards)} users")
    print("Sample rewards: ", dict(list(rewards.items())[:5]))
