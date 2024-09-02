import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from api.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_read_root(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Welcome to the Stride Airdrop API by MacBobby Chibuzor 🚀"})

    @patch('api.dependencies.get_db_manager')
    def test_get_summary(self, mock_get_db_manager):
        mock_db = MagicMock()
        mock_db.get_average_summary.return_value = {
            "average_staked": 1000,
            "average_eligible_users": 50,
            "max_stake": 5000
        }
        mock_get_db_manager.return_value = mock_db

        response = self.client.get("/api/summary")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "average_staked": 1000,
            "average_eligible_users": 50,
            "max_stake": 5000
        })

    @patch('api.dependencies.get_db_manager')
    def test_get_staked(self, mock_get_db_manager):
        mock_db = MagicMock()
        mock_db.get_user_stakes.return_value = [MagicMock(amount=1000), MagicMock(amount=2000)]
        mock_get_db_manager.return_value = mock_db

        response = self.client.get("/api/staked/test_address")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["amount"], 3000)

    @patch('api.dependencies.get_db_manager')
    def test_get_rewards(self, mock_get_db_manager):
        mock_db = MagicMock()
        mock_db.get_user_rewards.return_value = [MagicMock(amount=100), MagicMock(amount=200)]
        mock_get_db_manager.return_value = mock_db

        response = self.client.get("/api/rewards/test_address")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"address": "test_address", "amount": 300})


    @patch('api.dependencies.get_db')
    def test_claim_rewards(self, mock_get_db):
        mock_db = MagicMock()
        mock_db.claim_rewards.return_value = 500
        mock_get_db.return_value = mock_db

        response = self.client.post("/api/claim/test_address")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"address": "test_address", "claimed_amount": 500})

    @patch('api.dependencies.get_db')
    def test_claim_rewards_with_no_rewards(self, mock_get_db):
        mock_db = MagicMock()
        mock_db.claim_rewards.return_value = 0
        mock_get_db.return_value = mock_db

        response = self.client.post("/api/claim/test_address")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {"detail": "No rewards to claim"})

if __name__ == '__main__':
    unittest.main()