import requests
from typing import List, Dict
from pydantic import BaseModel

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
    delegations_response: List[DelegationResponse]
    pagination: Dict[str, str]


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

def process_delegations(validators: List[str]) -> Dict[str, Dict[str, int]]:
    user_delegations = {}

    for validator in validators:
        delegations = fetch_delegations(validator)
        for delegation in delegations:
            delegator = delegation.delegation.delegator_address
            amount = int(delegation.balance.amount)

            if delegator not in user_delegations:
                user_delegations[delegator] = {}

            user_delegations[delegator][validator] = amount

    return user_delegations

if __name__ == "__main__":
    from validator_scraper import fetch_validators

    validators = fetch_validators()
    validator_addresses = [v.operator_address for v in validators[:5]] # using the first 5 validators to test.
    user_delegations = process_delegations(validator_addresses)

    print(f"Total users with delegations: {len(user_delegations)}")
    for user, delegations in list(user_delegations.items())[:5]:
        print(f"User {user}: {delegations}")