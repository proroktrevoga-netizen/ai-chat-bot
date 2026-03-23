# AI Chat Bot

Телеграм-бот с ChatGPT (OpenAI API) и диалоговой памятью.

## Возможности

- Диалоговая память (последние 10 сообщений)
- Настраиваемый системный промпт
- Rate limiting (1 запрос в 3 секунды)
- Команды: /start, /clear, /system

## Запуск

```bash
cp .env.example .env
# Вставьте токены в .env
pip install -r requirements.txt
python bot.py
```

## Docker

```bash
docker build -t ai-chat-bot .
docker run --env-file .env ai-chat-bot
```

## Настройка

В `.env` можно изменить:
- `SYSTEM_PROMPT` — характер и стиль ответов бота
- `MAX_HISTORY` — сколько сообщений хранить в контексте
