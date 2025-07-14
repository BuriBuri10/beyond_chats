import os
from dotenv import load_dotenv
from pathlib import Path

root_path = Path(__file__).resolve().parents[1]
env_path = root_path / ".env"
load_dotenv(env_path)

print("client_id:", os.getenv("REDDIT_CLIENT_ID"))
print("client_secret:", os.getenv("REDDIT_CLIENT_SECRET"))
print("user_agent:", os.getenv("REDDIT_USER_AGENT"))

from logs.logging_config import logger

logger.info("Hello")
logger.error("This is an error")

