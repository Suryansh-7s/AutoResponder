import requests
import os
from dotenv import load_dotenv
load_dotenv()

# Replace with your token and chat ID
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }
    response = requests.post(url, data=payload)
    if response.status_code != 200:
        print(f"[!] Failed to send Telegram alert: {response.text}")
    else:
        print(f"[✓] Telegram alert sent: {message}")
