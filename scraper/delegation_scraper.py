import requests
from typing import List, Dict, Optional
from pydantic import BaseModel
from validator_scraper import fetch_validators
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Delegation(BaseModel):
    delegator_address: str
    validator_address: str
    shares: str

class Balance(BaseModel):
    denom: str
    amount: str

class DelegationResponse(BaseModel):
    delegation: Delegation
    balance: Balance

class DelegationsResponse(BaseModel):
    delegation_responses: List[DelegationResponse]
    pagination: Dict[str, Optional[str]]

BASE_URL = "https://stride-walk-214t-api.polkachu.com/cosmos/staking/v1beta1/validators/{}/delegations"

def fetch_delegations(validator_address: str) -> List[DelegationResponse]:
    delegations = []
    next_key = None

    while True:
        url = BASE_URL.format(validator_address)
        params = {"pagination.key": next_key} if next_key else {}
        response = requests.get(url, params=params)
        response.raise_for_status()

        data = DelegationsResponse(**response.json())
        delegations.extend(data.delegation_responses)

        next_key = data.pagination.get("next_key")
        if not next_key:
            break

    return delegations

def process_all_delegations() -> Dict[str, Dict[str, int]]:
    user_delegations = {}
    validators = fetch_validators()

    for validator in validators:
        logger.info(f"Fetching delegations for validator: {validator.operator_address}")
        delegations = fetch_delegations(validator.operator_address)
        for delegation in delegations:
            delegator = delegation.delegation.delegator_address
            amount = int(delegation.balance.amount)

            if delegator not in user_delegations:
                user_delegations[delegator] = {}

            user_delegations[delegator][validator.operator_address] = amount

    return user_delegations

if __name__ == "__main__":
    user_delegations = process_all_delegations()
    logger.info(f"Total users with delegations: {len(user_delegations)}")
    for user, delegations in list(user_delegations.items())[:5]:
        logger.info(f"User {user}: {delegations}")