import requests
import os

ACCESS_TOKEN = os.getenv("META_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def get_campaign_data():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": "campaign_name,reach,impressions,cpc,ctr,spend,cost_per_result",
        "date_preset": "today",
        "level": "campaign",
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()
    print("META RESPONSE:", res)

    if "data" not in res:
        raise Exception(f"Error Meta API: {res}")

    return res["data"]


def format_report(data):
    msg = "📊 Laporan Meta Ads Hari Ini\n\n"

    for camp in data:
        name = camp.get("campaign_name", "-")
        spend = float(camp.get("spend", 0))
        reach = camp.get("reach", 0)
        impressions = camp.get("impressions", 0)
        cpc = float(camp.get("cpc", 0))
        ctr = float(camp.get("ctr", 0))
        cpr = float(camp.get("cost_per_result", 0))

        msg += f"Campaign: {name}\n"
        msg += f"💰 Spend: Rp{spend:,.0f}\n"
        msg += f"👁 Reach: {reach}\n"
        msg += f"📊 Impressions: {impressions}\n"
        msg += f"🖱 CPC: Rp{cpc:,.0f}\n"
        msg += f"📈 CTR: {ctr}%\n"
        msg += f"🎯 CPR: Rp{cpr:,.0f}\n"
        msg += "------------------------\n"

    return msg


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }

    res = requests.post(url, data=data)
    print("TELEGRAM RESPONSE:", res.text)


def main():
    try:
        data = get_campaign_data()
        report = format_report(data)
        send_telegram(report)

    except Exception as e:
        print("ERROR:", e)
        send_telegram(f"❌ ERROR: {e}")


if __name__ == "__main__":
    main()
