import os
from dotenv import load_dotenv, find_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

SERVER_PORT = os.environ.get("SERVER_PORT", 42)
DB_TARGET_HOST = os.environ.get("DB_TARGET_HOST", 42)
GEN_LOG_LEVEL = os.environ.get("GEN_LOG_LEVEL", "WARNING").upper()
NUM_SIMILAR_USERS = int(os.getenv("NUM_SIMILAR_USERS", 0))

REGION_NAME="us-east-2"
S3_BUCKET="ml.personal.com"