import requests
import os

def main():
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    print("TOKEN:", TELEGRAM_TOKEN)
    print("CHAT_ID:", CHAT_ID)

    if not TELEGRAM_TOKEN or not CHAT_ID:
        raise Exception("TOKEN / CHAT_ID kosong")

    # ✅ URL WAJIB ADA TOKEN
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    print("URL:", url)  # debug penting

    data = {
        "chat_id": CHAT_ID,
        "text": "🔥 TEST FIX — HARUS MASUK!"
    }

    res = requests.post(url, data=data)

    print("STATUS:", res.status_code)
    print("RESPONSE:", res.text)

    if res.status_code != 200:
        raise Exception("Gagal kirim Telegram")

if __name__ == "__main__":
    main()
