import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime, UTC
from database.db_manager import DatabaseManager
from database.models import User, Stake, Reward, Claim, DailySummary

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_manager = DatabaseManager('sqlite:///:memory:')
        self.db_manager.create_tables()

    def test_store_stakes(self):
        stakes = {
            'user1': {'validator1': 1000, 'validator2': 2000},
            'user2': {'validator1': 1500}
        }
        date = datetime.now()
        self.db_manager.store_stakes(stakes, date)

        session = self.db_manager.get_session()
        users = session.query(User).all()
        stakes = session.query(Stake).all()
        session.close()

        self.assertEqual(len(users), 2)
        self.assertEqual(len(stakes), 3)


    def test_store_rewards(self):
        rewards = {'user1': 100, 'user2': 200}
        date = datetime.now()
        self.db_manager.store_rewards(rewards, date)

        session = self.db_manager.get_session()
        users = session.query(User).all()
        rewards = session.query(Reward).all()
        session.close()

        self.assertEqual(len(users), 2)
        self.assertEqual(len(rewards), 2)

    def test_store_daily_summary(self):
        summary = {
            'total_staked_balance': 10000,
            'average_staked': 5000,
            'largest_staked_balance': 7000,
            'total_users_with_balance': 2,
            'total_eligible_users': 2,
            'total_rewards': 300
        }
        date = datetime.now(UTC)
        self.db_manager.store_daily_summary(summary, date)

        session = self.db_manager.get_session()
        daily_summary = session.query(DailySummary).first()
        session.close()

        self.assertIsNotNone(daily_summary)
        self.assertEqual(daily_summary.total_staked, 10000)


    def test_get_user_stakes(self):
        user_address = 'user1'
        stakes = {user_address: {'validator1': 1000, 'validator2': 2000}}
        date = datetime.now()
        self.db_manager.store_stakes(stakes, date)

        user_stakes = self.db_manager.get_user_stakes(user_address, date)
        self.assertEqual(len(user_stakes), 2)
        self.assertEqual(sum(stake.amount for stake in user_stakes), 3000)


    def test_get_user_rewards(self):
        user_address = 'user1'
        rewards = {user_address: 100}
        date = datetime.now()
        self.db_manager.store_rewards(rewards, date)

        user_rewards = self.db_manager.get_user_rewards(user_address, date)
        self.assertEqual(len(user_rewards), 1)
        self.assertEqual(user_rewards[0].amount, 100)


    def test_claim_rewards(self):
        user_address = 'user1'
        rewards = {user_address: 100}
        date = datetime.now(UTC)
        self.db_manager.store_rewards(rewards, date)

        claimed_amount = self.db_manager.claim_rewards(user_address)
        self.assertEqual(claimed_amount, 100)

        session = self.db_manager.get_session()
        claim = session.query(Claim).first()
        session.close()

        self.assertIsNotNone(claim)
        self.assertEqual(claim.amount, 100)


    def test_get_daily_summary(self):
        summary = {
            'total_staked_balance': 10000,
            'average_staked': 5000,
            'largest_staked_balance': 7000,
            'total_users_with_balance': 2,
            'total_eligible_users': 2,
            'total_rewards': 300
        }
        date = datetime.now(UTC)
        self.db_manager.store_daily_summary(summary, date)

        daily_summary = self.db_manager.get_daily_summary(date)
        self.assertIsNotNone(daily_summary)
        self.assertEqual(daily_summary.total_staked, 10000)

    def test_get_average_summary(self):
        summary1 = {
            'total_staked_balance': 10000,
            'average_staked': 5000,
            'largest_staked_balance': 7000,
            'total_users_with_balance': 2,
            'total_eligible_users': 2,
            'total_rewards': 300
        }
        summary2 = {
            'total_staked_balance': 20000,
            'average_staked': 10000,
            'largest_staked_balance': 15000,
            'total_users_with_balance': 3,
            'total_eligible_users': 3,
            'total_rewards': 600
        }
        self.db_manager.store_daily_summary(summary1, datetime.now(UTC))
        self.db_manager.store_daily_summary(summary2, datetime.now(UTC))

        avg_summary = self.db_manager.get_average_summary()
        self.assertEqual(avg_summary['average_staked'], 7500)
        self.assertEqual(avg_summary['average_eligible_users'], 2.5)
        self.assertEqual(avg_summary['max_stake'], 15000)

if __name__ == '__main__':
    unittest.main()
