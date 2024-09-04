import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from reward_calculator.calculator import RewardCalculator
from reward_calculator.claim_tracker import ClaimTracker
from reward_calculator.summary_generator import SummaryGenerator

class TestRewardCalculator(unittest.TestCase):

    def setUp(self):
        self.mock_storage_manager = Mock()
        self.calculator = RewardCalculator(self.mock_storage_manager)

    def test_get_delegations(self):
        mock_delegations = {"user1": {"validator1": 1000000}}
        self.mock_storage_manager.retrieve_delegations.return_value = mock_delegations

        result = self.calculator.get_delegations()
        self.assertEqual(result, mock_delegations)

    def test_calculate_rewards(self):
        delegations = {
            "user1": {"validator1": 1000000000},  # 1000 STRD
            "user2": {"validator1": 900000000},   # 900 STRD
            "user3": {"validator1": 800000000},   # 800 STRD
            "user4": {"validator1": 460000000},   # 460 STRD
            "user5": {"validator1": 500000}       # 0.5 STRD
        }
        date = datetime.now().strftime("%Y-%m-%d")

        rewards = self.calculator.calculate_rewards(delegations, date)

        self.assertIn("user1", rewards)
        self.assertIn("user2", rewards)
        self.assertIn("user3", rewards)
        self.assertIn("user4", rewards)
        self.assertNotIn("user5", rewards)

    def test_claim_rewards(self):
        mock_rewards = {"user1": 1_000_000}
        self.calculator.process_rewards = Mock(return_value=(None, mock_rewards))
        self.calculator.claim_tracker.record_claims = Mock(return_value=True)

        reward = self.calculator.claim_reward("user1", "2023-08-30")
        self.assertEqual(reward, 2_000_000) # should be doubled reward for early claimer.


class TestClaimTracker(unittest.TestCase):

    def setUp(self):
        self.mock_storage_manager = Mock()
        self.claim_tracker = ClaimTracker(self.mock_storage_manager)


    def test_record_claims(self):
        self.claim_tracker.get_claims = Mock(return_value={})
        self.claim_tracker.save_claims = Mock()

        result = self.claim_tracker.record_claims("user1", "2023-08-30")
        self.assertTrue(result)


class TestSummaryGenerator(unittest.TestCase):

    def test_generate_summary(self):
        delegations = {
            "user1": {"validator1": 1_000_000_000},
            "user2": {"validator1": 900_000_000},
        }

        rewards = {"user1": 1_000_000, "user2": 900_000}
        mock_claim_tracker = Mock()
        mock_claim_tracker.get_early_claimers_count.return_value = 1

        summary = SummaryGenerator.generate_summary(delegations, rewards, mock_claim_tracker, "2023-08-30")

        self.assertEqual(summary["total_staked_balance"], 1900000000)
        self.assertEqual(summary["largest_staked_balance"], 1000000000)
        self.assertEqual(summary["total_users_with_balance"], 2)
        self.assertEqual(summary["total_eligible_users"], 2)
        self.assertEqual(summary["early_claimers"], 1)



if __name__ == "__main__":
    unittest.main()
