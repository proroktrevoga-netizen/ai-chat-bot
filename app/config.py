import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SYSTEM_PROMPT = os.getenv("SYSTEM_PROMPT", "Ты полезный AI-ассистент. Отвечай кратко и по делу.")
MAX_HISTORY = int(os.getenv("MAX_HISTORY", "10"))

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set")
