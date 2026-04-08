import requests
import os

ACCESS_TOKEN = os.getenv("META_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def format_rp(value):
    try:
        return f"Rp{int(float(value)):,}".replace(",", ".")
    except:
        return "Rp0"


def get_insights():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": "campaign_name,reach,impressions,ctr,cpc,spend,actions",
        "access_token": ACCESS_TOKEN,
        "date_preset": "today"
    }

    res = requests.get(url, params=params).json()
    print("META RESPONSE:", res)

    return res.get("data", [])


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


# 🔥 SAFE PURCHASE (ANTI ERROR)
def get_purchase(actions):
    if not actions:
        return "-"

    for act in actions:
        if act.get("action_type") == "purchase":
            try:
                return int(float(act.get("value", 0)))
            except:
                return "-"

    return "-"


def format_report(data, balance):
    text = f"📊 META ADS REPORT HARI INI\n\n"
    text += f"🏢 Account: {AD_ACCOUNT_ID}\n"
    text += f"💰 Saldo: {format_rp(balance)}\n\n"

    if not data:
        return text + "⚠️ Tidak ada data campaign"

    for item in data[:5]:
        ctr = float(item.get("ctr", 0))
        cpc = item.get("cpc", 0)
        spend = item.get("spend", 0)

        purchase = get_purchase(item.get("actions"))

        text += f"📌 {item.get('campaign_name','-')}\n"
        text += f"Reach: {item.get('reach','-')}\n"
        text += f"Impression: {item.get('impressions','-')}\n"
        text += f"CTR: {ctr:.2f}%\n"
        text += f"CPC: {format_rp(cpc)}\n"
        text += f"Spend: {format_rp(spend)}\n"
        text += f"Purchase: {purchase}\n\n"

    return text


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    res = requests.post(url, data=data)
    print("TELEGRAM:", res.text)


def main():
    print("SCRIPT START")

    insights = get_insights()
    balance = get_balance()

    report = format_report(insights, balance)

    print("REPORT:", report)

    send_telegram(report)


if __name__ == "__main__":
    main()
