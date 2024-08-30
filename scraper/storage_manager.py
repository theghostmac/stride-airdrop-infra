import json
import boto3
from botocore.exceptions import ClientError
from typing import Dict

class StorageManager:
    def __init__(self, bucket_name: str):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name


    def store_delegations(self, delegations: Dict[str, Dict[str, int]], date: str):
        try:
            file_name = f"delegations_{date}.json"
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=json.dumps(delegations),
                ContentType='application/json'
            )
            print(f"Successfully stored delegations for {date}")
        except ClientError as e:
            print(f"Error storing delegations: {e}")


    def retrieve_delegations(self, date: str) -> Dict[str, Dict[str, int]]:
        try:
            file_name = f"delegations_{date}.json"
            response = self.s3.get_object(
                Bucket=self.bucket_name,
                Key=file_name,
            )
            return json.loads(response['Body'].read().decode('utf-8'))
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                print(f"No delegations found for {date}")
                return {}
            else:
                print(f"Error retrieving delegations: {e}")
                raise

    def store_file(self, file_name: str, content: str):
        try:
            self.s3.put_object(
                Bucket=self.bucket_name,
                Key=file_name,
                Body=content,
                ContentType='application/json',
            )
        except Exception as e:
            print(f"Error storing file {file_name}: {e}")


if __name__ == "__main__":
    # For testing purposes
    storage = StorageManager('stride-airdrop-bucket')
    test_delegations = {
        "user1": {"validator1": 1000, "validator2": 2000},
        "user2": {"validator1": 1500, "validator3": 3000}
    }
    storage.store_delegations(test_delegations, "2023-08-29")
    retrieved = storage.retrieve_delegations("2023-08-29")
    print(f"Retrieved delegations: {retrieved}")