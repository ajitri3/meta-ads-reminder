import requests
import os

ACCESS_TOKEN = os.getenv("META_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

THRESHOLD = 200000  # batas saldo (Rp)

def get_balance():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}"
    params = {
        "fields": "balance",
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()
    print("META RESPONSE:", res)

    if "balance" not in res:
        raise Exception(f"Balance not found: {res}")

    return int(res["balance"]) / 100


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    res = requests.post(url, data=data)
    print("TELEGRAM RESPONSE:", res.text)


def main():
    print("DEBUG TOKEN:", TELEGRAM_TOKEN)
    print("DEBUG CHAT_ID:", CHAT_ID)
    print("DEBUG AD_ACCOUNT_ID:", AD_ACCOUNT_ID)

    balance = get_balance()
    print(f"Saldo sekarang: Rp{balance:,.0f}")

    if balance < THRESHOLD:
        send_telegram(f"⚠️ Saldo Meta Ads tinggal Rp{balance:,.0f}")
    else:
        send_telegram(f"✅ Saldo aman: Rp{balance:,.0f}")


if __name__ == "__main__":
    main()
