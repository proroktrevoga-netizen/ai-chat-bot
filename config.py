import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ["BOT_TOKEN"]
OPENAI_API_KEY: str = os.environ["OPENAI_API_KEY"]

SYSTEM_PROMPT: str = os.getenv(
    "SYSTEM_PROMPT",
    "You are a helpful assistant. Answer clearly and concisely.",
)

MAX_HISTORY: int = int(os.getenv("MAX_HISTORY", "10"))
OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
RATE_LIMIT_SECONDS: float = float(os.getenv("RATE_LIMIT_SECONDS", "3"))
