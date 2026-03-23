import asyncio
import logging
import time
from collections import defaultdict

from aiogram import Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.types import Message
from openai import AsyncOpenAI

from config import BOT_TOKEN, MAX_HISTORY, OPENAI_API_KEY, SYSTEM_PROMPT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

user_histories: dict[int, list[dict]] = defaultdict(list)
user_last_request: dict[int, float] = {}
RATE_LIMIT_SEC = 3


def get_history(user_id: int) -> list[dict]:
    return user_histories[user_id][-MAX_HISTORY * 2:]


@router.message(Command("start"))
async def cmd_start(message: Message):
    user_histories[message.from_user.id].clear()
    await message.answer(
        "Привет! Я AI-ассистент. Напиши мне что-нибудь.\n"
        "/clear — очистить историю\n"
        "/system — текущий системный промпт"
    )


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    user_histories[message.from_user.id].clear()
    await message.answer("История очищена.")


@router.message(Command("system"))
async def cmd_system(message: Message):
    await message.answer(f"Системный промпт:\n\n{SYSTEM_PROMPT}")


@router.message()
async def handle_message(message: Message):
    if not message.text:
        return

    user_id = message.from_user.id
    now = time.time()

    if now - user_last_request.get(user_id, 0) < RATE_LIMIT_SEC:
        await message.answer("Подожди немного перед следующим запросом.")
        return

    user_last_request[user_id] = now
    user_histories[user_id].append({"role": "user", "content": message.text})

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + get_history(user_id)

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=1000,
        )
        reply = response.choices[0].message.content
        user_histories[user_id].append({"role": "assistant", "content": reply})
        await message.answer(reply)
    except Exception as e:
        logger.error(f"OpenAI error: {e}")
        await message.answer("Произошла ошибка. Попробуй позже.")


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    logger.info("AI Chat Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
