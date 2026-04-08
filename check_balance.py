import requests
import os
print("AD_ACCOUNT_ID:", AD_ACCOUNT_ID)
ACCESS_TOKEN = os.getenv("META_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

THRESHOLD = 200000


def get_balance():
    url = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}"
    params = {
        "fields": "balance",
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()

    if "balance" not in res:
        print("ERROR RESPONSE:", res)
        raise Exception("Balance not found")

    return int(res["balance"]) / 100


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)


def main():
    balance = get_balance()
    print("Balance:", balance)  # debug biar keliatan di GitHub

    if balance < THRESHOLD:
        send_telegram(f"⚠️ Saldo Meta Ads tinggal Rp{balance:,.0f}")
    else:
        print("Saldo masih aman")


if __name__ == "__main__":
    main()
