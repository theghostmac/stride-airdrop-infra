import requests
from typing import List, Dict
from pydantic import BaseModel

class Validator(BaseModel):
    operator_address: str
    # TODO: adding other fields when needed.


class ValidatorResponse(BaseModel):
    validators: List[Validator]
    pagination: Dict[str, str]


BASE_URL = "https://stride-walk-214t-api.polkachu.com/cosmos/staking/v1beta1/validators"

def fetch_validators() -> List[Validator]:
    validators = []
    next_key = None

    while True:
        params = {"pagination.key": next_key} if next_key else {}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()

        data = ValidatorResponse(**response.json())
        validators.extend(data.validators)

        next_key = data.pagination.get("next_key")
        if not next_key:
            break

    return validators


if __name__ == "__main__":
    validators = fetch_validators()
    print(f"Total validators fetched: {len(validators)}")
    for validator in validators:
        print(validator.operator_address)