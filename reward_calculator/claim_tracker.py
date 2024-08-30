from typing import Dict, List
import json
from datetime import datetime

class ClaimTracker:
    def __init__(self, storage_member):
        self.storage_member = storage_member
        self.claim_file = "claims.json"
        self.max_early_claims = 100


    def get_claims(self) -> Dict[str, List[str]]:
        try:
            claims_data = self.storage_member.retrieve_file(self.claim_file)
            return json.loads(claims_data)
        except Exception:
            return {}


    def save_claims(self, claims :Dict[str, List[str]]):
        self.storage_member.store_file(self.claim_file, json.dumps(claims))


    def record_claims(self, address: str, date: str) -> bool:
        claims = self.get_claims()
        if date not in claims:
            claims[date] = []

        if address not in claims[date] and len(claims[date]) < self.max_early_claims:
            claims[date].append(address)
            self.save_claims(claims)
            return True
        return False

    def is_early_claimer(self, address: str, date: str) -> bool:
        claims = self.get_claims()
        return date in claims and address in claims[date]


    def get_early_claimers_count(self, date: str) -> int:
        claims = self.get_claims()
        return len(claims.get(date, []))