import os
from dotenv import load_dotenv, find_dotenv
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

NUM_SIMILAR_USERS = int(os.getenv('NUM_SIMILAR_USERS', 0))
GEN_LOG_LEVEL = os.environ.get('GEN_LOG_LEVEL', 'WARNING').upper()