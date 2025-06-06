import os
import time
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise RuntimeError("Please set the TELEGRAM_TOKEN environment variable")

API_URL = f"https://api.telegram.org/bot{TOKEN}"

# In-memory pet state per chat
pets = {}


def get_updates(offset=None):
    params = {"timeout": 100}
    if offset:
        params["offset"] = offset
    r = requests.get(f"{API_URL}/getUpdates", params=params)
    r.raise_for_status()
    return r.json().get("result", [])


def send_message(chat_id: int, text: str):
    requests.post(f"{API_URL}/sendMessage", data={"chat_id": chat_id, "text": text})


def update_pet(pet: dict):
    now = time.time()
    elapsed_hours = int((now - pet["last_update"]) / 3600)
    if elapsed_hours:
        pet["hunger"] = max(0, pet["hunger"] - elapsed_hours)
        pet["happiness"] = max(0, pet["happiness"] - elapsed_hours)
        pet["last_update"] = now


def handle_update(update: dict):
    message = update.get("message")
    if not message:
        return

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if chat_id not in pets:
        pets[chat_id] = {"hunger": 5, "happiness": 5, "last_update": time.time()}

    pet = pets[chat_id]
    update_pet(pet)

    if text == "/start":
        send_message(chat_id, "Welcome to Telegram Tamagotchi! Use /feed, /play, /status.")
    elif text == "/feed":
        pet["hunger"] = min(10, pet["hunger"] + 3)
        send_message(chat_id, "You fed your pet!")
    elif text == "/play":
        pet["happiness"] = min(10, pet["happiness"] + 3)
        send_message(chat_id, "You played with your pet!")
    elif text == "/status":
        send_message(chat_id, f"Hunger: {pet['hunger']}/10\nHappiness: {pet['happiness']}/10")
    else:
        send_message(chat_id, "Unknown command. Use /feed, /play, /status.")


def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        for upd in updates:
            handle_update(upd)
            last_update_id = upd["update_id"] + 1
        time.sleep(1)


if __name__ == "__main__":
    main()
