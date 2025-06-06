# Telegram Tamagotchi

This repository contains a simple Tamagotchi-style game that works as a Telegram bot using the Web API.

## Getting Started

1. Create a new bot with [BotFather](https://t.me/BotFather) to obtain a token.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set the environment variable `TELEGRAM_TOKEN` with your bot token or edit `tamagotchi_bot.py` to include it.
4. Run the bot:
   ```bash
   python tamagotchi_bot.py
   ```

## Commands

- `/start` – initialize the pet and get instructions.
- `/status` – show the current hunger and happiness levels.
- `/feed` – feed the pet and reduce hunger.
- `/play` – play with the pet and increase happiness.

The bot stores state in memory per chat, so if it restarts the pet resets.
