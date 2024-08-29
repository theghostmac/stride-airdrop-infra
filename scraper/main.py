from datetime import datetime
from validator_scraper import fetch_validators
from delegation_scraper import process_delegations
from storage_manager import StorageManager

def main():
    # init StorageManager
    storage = StorageManager("test-bucket-name")

    # fetch validators
    validators = fetch_validators()
    validator_addresses = [v.operator_address for v in validators]

    # process delegation
    user_delegations = process_delegations(validator_addresses)

    # store delegations
    today = datetime.utcnow().strftime("%Y-%m-%d")
    storage.store_delegations(user_delegations, today)


if __name__ == "__main__":
    main()