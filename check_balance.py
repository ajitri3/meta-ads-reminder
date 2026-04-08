import requests
import os

def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    print("TOKEN:", TELEGRAM_TOKEN)
    print("CHAT_ID:", CHAT_ID)

    if not TELEGRAM_TOKEN or not CHAT_ID:
        raise Exception("TOKEN / CHAT_ID kosong")

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": "🔥 TEST GITHUB MASUK"
    }

    res = requests.post(url, data=data)

    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)

if __name__ == "__main__":
    main()
