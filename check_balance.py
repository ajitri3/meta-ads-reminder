import requests
import os

ACCESS_TOKEN = os.getenv("META_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def get_insights():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": "campaign_name,reach,impressions,ctr,cpc,cost_per_result",
        "access_token": ACCESS_TOKEN,
        "date_preset": "today"
    }

    res = requests.get(url, params=params).json()

    print("META RESPONSE:", res)

    if "data" not in res:
        raise Exception("Gagal ambil data Meta")

    return res["data"]


def get_balance():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}"

    params = {
        "fields": "balance",
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()

    print("BALANCE RESPONSE:", res)

    if "balance" not in res:
        return 0

    return int(res["balance"]) / 100


def format_report(data, balance):
    text = f"📊 META ADS REPORT\n\n💰 Saldo: Rp{balance:,.0f}\n\n"

    for item in data[:5]:  # ambil max 5 campaign
        text += f"📌 {item.get('campaign_name','-')}\n"
        text += f"Reach: {item.get('reach','-')}\n"
        text += f"Impression: {item.get('impressions','-')}\n"
        text += f"CTR: {item.get('ctr','-')}%\n"
        text += f"CPC: Rp{item.get('cpc','-')}\n"
        text += f"Cost/Result: Rp{item.get('cost_per_result','-')}\n\n"

    return text


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    requests.post(url, data=data)


def main():
    insights = get_insights()
    balance = get_balance()

    report = format_report(insights, balance)

    send_telegram(report)


if __name__ == "__main__":
    main()
