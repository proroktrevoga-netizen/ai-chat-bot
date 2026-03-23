import asyncio
import logging
import time
from collections import defaultdict, deque
from typing import Deque

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from openai import AsyncOpenAI

import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

# --- State ---

# history[user_id] = deque of {"role": ..., "content": ...}
history: dict[int, Deque[dict]] = defaultdict(lambda: deque(maxlen=config.MAX_HISTORY * 2))

# last_request[user_id] = timestamp
last_request: dict[int, float] = {}

# --- Clients ---

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()
openai_client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)


# --- Helpers ---

def is_rate_limited(user_id: int) -> float:
    """Returns remaining wait seconds, or 0 if allowed."""
    last = last_request.get(user_id, 0)
    elapsed = time.monotonic() - last
    remaining = config.RATE_LIMIT_SECONDS - elapsed
    return max(0.0, remaining)


def build_messages(user_id: int) -> list[dict]:
    msgs = [{"role": "system", "content": config.SYSTEM_PROMPT}]
    msgs.extend(history[user_id])
    return msgs


# --- Handlers ---

@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(
        "👋 Hi! I'm an AI assistant powered by OpenAI.\n\n"
        "Just send me a message and I'll reply.\n\n"
        "Commands:\n"
        "/clear — reset conversation history\n"
        "/system — show current system prompt"
    )


@dp.message(Command("clear"))
async def cmd_clear(message: Message) -> None:
    user_id = message.from_user.id
    history[user_id].clear()
    await message.answer("🗑 History cleared. Starting fresh!")


@dp.message(Command("system"))
async def cmd_system(message: Message) -> None:
    await message.answer(f"<b>System prompt:</b>\n<code>{config.SYSTEM_PROMPT}</code>", parse_mode="HTML")


@dp.message(F.text)
async def handle_message(message: Message) -> None:
    user_id = message.from_user.id

    wait = is_rate_limited(user_id)
    if wait > 0:
        await message.answer(f"⏳ Please wait {wait:.1f}s before sending another message.")
        return

    last_request[user_id] = time.monotonic()

    user_text = message.text.strip()
    history[user_id].append({"role": "user", "content": user_text})

    thinking = await message.answer("...")

    try:
        response = await openai_client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=build_messages(user_id),
        )
        reply = response.choices[0].message.content
        history[user_id].append({"role": "assistant", "content": reply})
        await thinking.edit_text(reply)
    except Exception as e:
        logger.error("OpenAI error for user %d: %s", user_id, e)
        history[user_id].pop()  # remove the unanswered user message
        await thinking.edit_text("⚠️ Something went wrong. Please try again.")


# --- Entry point ---

async def main() -> None:
    logger.info("Starting bot (model=%s, max_history=%d)", config.OPENAI_MODEL, config.MAX_HISTORY)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
