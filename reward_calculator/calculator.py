from typing import Dict, List, Tuple

from reward_calculator.claim_tracker import ClaimTracker
from scraper.storage_manager import StorageManager
from datetime import datetime, timedelta


class RewardCalculator:
    def __init__(self, storage_manager: StorageManager):
        self.storage_manager = storage_manager
        self.claim_tracker = ClaimTracker(storage_manager)
        self.total_daily_reward = 1_000_000 * 1_000_000  # 1M STRD in ustrd is the fixed reward to stakers, daily.


    def get_delegations(self, date: str = None) -> Dict[str, Dict[str, int]]:
        if date is None:
            date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        return self.storage_manager.retrieve_delegations(date)


    def calculate_rewards(self, delegations: Dict[str, Dict[str, int]], date: str) -> Dict[str, int]:
        total_staked = sum(sum(user_delegations.values()) for user_delegations in delegations.values())
        eligible_users = {user: sum(stakes.values()) for user, stakes in delegations.items() if sum(stakes.values()) >= 1_000_000}

        if not eligible_users:
            return {}

        sorted_users = sorted(eligible_users.items(), key=lambda x: x[1], reverse=True)
        top_1_percent = max(1, int(len(sorted_users) * 0.01))
        top_5_percent = max(1, int(len(sorted_users) * 0.05))

        rewards = {}
        for i, (user, stake) in enumerate(sorted_users):
            base_reward = (stake / total_staked) * self.total_daily_reward
            if i < top_1_percent:
                multiplier = 2
            elif i < top_5_percent:
                multiplier = 1.5
            else:
                multiplier = 1

            if self.claim_tracker.is_early_claimer(user, date):
                multiplier *= 2

            rewards[user] = int(base_reward * multiplier)

        return rewards


    def process_rewards(self, date: str = None) -> Tuple[Dict[str, Dict[str, int]], Dict[str, int]]:
        if date is None:
            date = (datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d")
        delegations = self.get_delegations(date)
        rewards = self.calculate_rewards(delegations, date)
        return delegations, rewards


    def claim_reward(self, address: str, date: str) -> int:
        delegations, rewards = self.process_rewards(date)
        if address in rewards:
            reward = rewards[address]
            if self.claim_tracker.record_claim(address, date):
                reward *= 2  # Double the reward for early claimers
            return reward
        return 0


if __name__ == "__main__":
    storage_manager = StorageManager("stride-airdrop-bucket")
    calculator = RewardCalculator(storage_manager)
    date = datetime.utcnow().strftime("%Y-%m-%d")
    delegations, rewards = calculator.process_rewards()
    print(f"Processed rewards for {len(rewards)} users")
    print("Sample rewards: ", dict(list(rewards.items())[:5]))

    # simulating some claims
    for address in list(rewards.keys())[:10]:
        claimed_rewards = calculator.claim_reward(address, date)
        print(f"Address {address} claimed {claimed_rewards} ustrd")

