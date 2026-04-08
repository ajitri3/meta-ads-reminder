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
        "fields": "campaign_name,reach,impressions,ctr,cpc,spend,purchase_roas,actions,action_values",
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


# 🔥 MULTI EVENT (ANTI META NGACO)
def extract_value_multi(data_list, keys):
    if not data_list:
        return 0

    for key in keys:
        for item in data_list:
            if item.get("action_type") == key:
                return float(item.get("value", 0))

    return 0


# 🔥 CPAS + WEBSITE SAFE
def get_purchase(actions):
    return extract_value_multi(actions, [
        "offsite_conversion.omni_purchase",
        "omni_purchase",
        "offsite_conversion.purchase",
        "purchase"
    ])


def get_purchase_value(values):
    return extract_value_multi(values, [
        "offsite_conversion.omni_purchase",
        "omni_purchase",
        "offsite_conversion.purchase",
        "purchase"
    ])


def get_roas(item):
    if item.get("purchase_roas"):
        try:
            return float(item["purchase_roas"][0].get("value", 0))
        except:
            return 0
    return 0


def format_report(data, balance):
    text = f"📊 META ADS REPORT HARI INI\n\n"
    text += f"🏢 Account: {AD_ACCOUNT_ID}\n"
    text += f"💰 Saldo: {format_rp(balance)}\n\n"

    if not data:
        return text + "⚠️ Tidak ada data campaign"

    total_spend = 0
    total_purchase = 0
    total_revenue = 0

    for item in data[:5]:
        ctr = float(item.get("ctr", 0))
        cpc = item.get("cpc", 0)
        spend = float(item.get("spend", 0))

        purchase = get_purchase(item.get("actions"))
        purchase_value = get_purchase_value(item.get("action_values"))
        roas = get_roas(item)

        total_spend += spend
        total_purchase += purchase
        total_revenue += purchase_value

        text += f"📌 {item.get('campaign_name','-')}\n"
        text += f"Reach: {item.get('reach','-')}\n"
        text += f"Impression: {item.get('impressions','-')}\n"
        text += f"CTR: {ctr:.2f}%\n"
        text += f"CPC: {format_rp(cpc)}\n"
        text += f"Spend: {format_rp(spend)}\n"
        text += f"Purchase: {int(purchase)}\n"
        text += f"Revenue: {format_rp(purchase_value)}\n"
        text += f"ROAS: {roas:.2f}\n\n"

    # 🔥 TOTAL
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
    print("TELEGRAM:", res.text)


def main():
    insights = get_insights()
    balance = get_balance()

    report = format_report(insights, balance)
    print(report)

    send_telegram(report)


if __name__ == "__main__":
    main()
