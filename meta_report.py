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


def get_account_name():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}"
    params = {
        "fields": "name",
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()
    print("ACCOUNT RESPONSE:", res)

    return res.get("name", "Unknown Account")


def get_insights():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": "campaign_name,reach,impressions,ctr,cpc,spend,actions,action_values",
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


def get_purchase(actions):
    total = 0
    if not actions:
        return 0

    for act in actions:
        if act.get("action_type") == "purchase":
            total += float(act.get("value", 0))

    return total


def get_purchase_value(action_values):
    total = 0
    if not action_values:
        return 0

    for val in action_values:
        if val.get("action_type") == "purchase":
            total += float(val.get("value", 0))

    return total


def get_roas(item):
    spend = float(item.get("spend") or 0)
    revenue = get_purchase_value(item.get("action_values"))

    if spend == 0:
        return 0

    return revenue / spend


def format_report(data, balance, account_name):
    text = f"📊 META ADS REPORT HARI INI\n\n"
    text += f"🏢 Account: {account_name}\n"
    text += f"💰 Saldo: {format_rp(balance)}\n\n"

    if not data:
        return text + "⚠️ Tidak ada data campaign"

    total_spend = 0
    total_purchase = 0
    total_revenue = 0

    for item in data[:5]:
        try:
            ctr = float(item.get("ctr") or 0)
            cpc = float(item.get("cpc") or 0)
            spend = float(item.get("spend") or 0)

            purchase = get_purchase(item.get("actions"))
            revenue = get_purchase_value(item.get("action_values"))
            roas = get_roas(item)

        except Exception as e:
            print("ERROR ITEM:", e)
            continue

        total_spend += spend
        total_purchase += purchase
        total_revenue += revenue

        text += f"📌 {item.get('campaign_name','-')}\n"
        text += f"Reach: {item.get('reach','-')}\n"
        text += f"Impression: {item.get('impressions','-')}\n"
        text += f"CTR: {ctr:.2f}%\n"
        text += f"CPC: {format_rp(cpc)}\n"
        text += f"Spend: {format_rp(spend)}\n"
        text += f"🛒 Purchase: {int(purchase)}\n"
        text += f"💵 Revenue: {format_rp(revenue)}\n"
        text += f"📈 ROAS: {roas:.2f}\n\n"

    total_roas = total_revenue / total_spend if total_spend > 0 else 0

    text += f"========== TOTAL ==========\n"
    text += f"Spend: {format_rp(total_spend)}\n"
    text += f"Purchase: {int(total_purchase)}\n"
    text += f"Revenue: {format_rp(total_revenue)}\n"
    text += f"ROAS: {total_roas:.2f}\n"

    return text


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    res = requests.post(url, data=data)

    print("TELEGRAM STATUS:", res.status_code)
    print("TELEGRAM RESPONSE:", res.text)


def main():
    print("SCRIPT START")

    insights = get_insights()
    print("INSIGHTS:", insights)

    balance = get_balance()
    print("BALANCE:", balance)

    account_name = get_account_name()
    print("ACCOUNT:", account_name)

    report = format_report(insights, balance, account_name)
    print("REPORT:", report)

    send_telegram(report)


if __name__ == "__main__":
    main()
