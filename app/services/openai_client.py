import logging
from collections import defaultdict

from openai import AsyncOpenAI

from app.config import OPENAI_API_KEY, SYSTEM_PROMPT, MAX_HISTORY

logger = logging.getLogger(__name__)

client = AsyncOpenAI(api_key=OPENAI_API_KEY)
user_histories: dict[int, list[dict]] = defaultdict(list)


def get_history(user_id: int) -> list[dict]:
    return user_histories[user_id][-MAX_HISTORY * 2:]


def clear_history(user_id: int):
    user_histories[user_id].clear()


async def get_response(user_id: int, text: str) -> str:
    user_histories[user_id].append({"role": "user", "content": text})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(user_id)
    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
        )
        reply = response.choices[0].message.content
        user_histories[user_id].append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        user_histories[user_id].pop()  # убираем неудачный запрос
        logger.error(f"OpenAI error: {e}")
        raise
