import os
import boto3
import json
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables in local development
load_dotenv()

def get_mongo_credentials():
    if os.getenv("AWS_LAMBDA_FUNCTION_NAME"):  # Running in AWS Lambda
        secret_name = os.getenv("AWS_SECRET_NAME", "mongo_credentials")
        region_name = os.getenv("AWS_REGION", "us-east-1")

        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=region_name)
        
        # Retrieve and parse the secret
        secret_value = client.get_secret_value(SecretId=secret_name)
        secret_dict = json.loads(secret_value["SecretString"])
        
        return secret_dict["uri"], secret_dict["db_name"]
    
    # Running locally - Fetch credentials from environment variables
    return os.getenv("MONGO_URI", "mongodb://localhost:27017"), os.getenv("MONGO_DB_NAME", "company_db")

# Get MongoDB connection details
MONGO_URI, DB_NAME = get_mongo_credentials()

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_employee_collection():
    return db["employees"]
