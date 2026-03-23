# AI Chat Bot

Telegram bot with OpenAI GPT integration. Maintains conversation context, supports system prompt configuration, and includes per-user rate limiting.

## Features

- **Conversation memory** — keeps last 10 message pairs in context per user
- **Configurable system prompt** — set via environment variable
- **Rate limiting** — 1 request per 3 seconds per user (configurable)
- **Commands**: `/start`, `/clear`, `/system`
- **Docker-ready**

## Quick Start

```bash
cp .env.example .env
# Fill in BOT_TOKEN and OPENAI_API_KEY

pip install -r requirements.txt
python bot.py
```

## Docker

```bash
docker build -t ai-chat-bot .
docker run --env-file .env ai-chat-bot
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `BOT_TOKEN` | required | Telegram bot token |
| `OPENAI_API_KEY` | required | OpenAI API key |
| `SYSTEM_PROMPT` | see config.py | Assistant personality |
| `MAX_HISTORY` | 10 | Message pairs kept in context |
| `OPENAI_MODEL` | gpt-4o-mini | OpenAI model |
| `RATE_LIMIT_SECONDS` | 3 | Min seconds between requests per user |

## Stack

- Python 3.11
- [aiogram](https://github.com/aiogram/aiogram) 3.x
- [openai](https://github.com/openai/openai-python) 1.x
