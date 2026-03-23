from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.config import SYSTEM_PROMPT
from app.services.openai_client import get_response, clear_history
from app.services.rate_limiter import check_rate_limit

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    clear_history(message.from_user.id)
    await message.answer(
        "Привет! Я AI-ассистент. Напиши мне что-нибудь.\n"
        "/clear — очистить историю\n"
        "/system — текущий системный промпт"
    )


@router.message(Command("clear"))
async def cmd_clear(message: Message):
    clear_history(message.from_user.id)
    await message.answer("История очищена.")


@router.message(Command("system"))
async def cmd_system(message: Message):
    await message.answer(f"Системный промпт:\n\n{SYSTEM_PROMPT}")


@router.message()
async def handle_message(message: Message):
    if not message.text:
        return
    if not check_rate_limit(message.from_user.id):
        await message.answer("Подожди немного перед следующим запросом.")
        return
    try:
        reply = await get_response(message.from_user.id, message.text)
        await message.answer(reply)
    except Exception:
        await message.answer("Произошла ошибка. Попробуй позже.")
