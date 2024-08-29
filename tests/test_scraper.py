import unittest
from unittest.mock import patch, MagicMock
from scraper.validator_scraper import fetch_validators, Validator
from scraper.delegation_scraper import fetch_delegations, process_delegations
from scraper.storage_manager import StorageManager
from typing import Optional


class TestScraper(unittest.TestCase):

    @patch('scraper.validator_scraper.requests.get')
    def test_fetch_validators(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "validators": [{"operator_address": "validator1"}, {"operator_address": "validator2"}],
            "pagination": {"next_key": None}
        }
        mock_get.return_value = mock_response

        validators = fetch_validators()
        self.assertEqual(len(validators), 2)
        self.assertIsInstance(validators[0], Validator)

    @patch('scraper.delegation_scraper.requests.get')
    def test_fetch_delegations(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "delegation_responses": [
                {
                    "delegation": {
                        "delegator_address": "delegator1",
                        "validator_address": "validator1",
                        "shares": "1000"
                    },
                    "balance": {"denom": "ustrd", "amount": "1000"}
                }
            ],
            "pagination": {"next_key": None}
        }
        mock_get.return_value = mock_response

        delegations = fetch_delegations("validator1")
        self.assertEqual(len(delegations), 1)

    @patch('scraper.delegation_scraper.fetch_delegations')
    def test_process_delegations(self, mock_fetch_delegations):
        mock_fetch_delegations.return_value = [
            MagicMock(
                delegation=MagicMock(delegator_address="delegator1"),
                balance=MagicMock(amount="1000")
            )
        ]

        result = process_delegations(["validator1"])
        self.assertIn("delegator1", result)
        self.assertEqual(result["delegator1"]["validator1"], 1000)

    @patch('scraper.storage_manager.boto3.client')
    def test_storage_manager(self, mock_boto3_client):
        mock_s3 = MagicMock()
        mock_boto3_client.return_value = mock_s3

        storage = StorageManager("test-bucket")
        test_data = {"user1": {"validator1": 1000}}

        storage.store_delegations(test_data, "2023-08-29")
        mock_s3.put_object.assert_called_once()

        mock_s3.get_object.return_value = {'Body': MagicMock(read=lambda: b'{"user1": {"validator1": 1000}}')}
        retrieved_data = storage.retrieve_delegations("2023-08-29")
        self.assertEqual(retrieved_data, test_data)

if __name__ == '__main__':
    unittest.main()