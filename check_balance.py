import requests
import os

ACCESS_TOKEN = os.getenv("META_TOKEN")
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def get_campaign_data():
    url = f"https://graph.facebook.com/v18.0/{AD_ACCOUNT_ID}/insights"

    params = {
        "fields": "campaign_name,reach,impressions,cpc,ctr,spend",
        "date_preset": "today",  # REALTIME HARI INI
        "level": "campaign",
        "access_token": ACCESS_TOKEN
    }

    res = requests.get(url, params=params).json()
    print("META RESPONSE:", res)

    if "data" not in res:
        raise Exception(f"Error Meta API: {res}")

    return res["data"]


def format_report(data):
    if len(data) == 0:
        return "⚠️ Tidak ada data campaign hari ini (belum ada spend)"

    total_spend = 0
    total_reach = 0
    total_impressions = 0

    msg = "📊 REALTIME META ADS (HARI INI)\n\n"

    for camp in data:
        name = camp.get("campaign_name", "-")
        spend = float(camp.get("spend", 0))
        reach = int(camp.get("reach", 0))
        impressions = int(camp.get("impressions", 0))
        cpc = float(camp.get("cpc", 0))
        ctr = float(camp.get("ctr", 0))

        total_spend += spend
        total_reach += reach
        total_impressions += impressions

        msg += f"🚀 {name}\n"
        msg += f"💰 Spend: Rp{spend:,.0f}\n"
        msg += f"👁 Reach: {reach:,}\n"
        msg += f"📊 Impressions: {impressions:,}\n"
        msg += f"🖱 CPC: Rp{cpc:,.0f}\n"
        msg += f"📈 CTR: {ctr}%\n"
        msg += "----------------------\n"

    msg += "\n📌 TOTAL\n"
    msg += f"💰 Total Spend: Rp{total_spend:,.0f}\n"
    msg += f"👁 Total Reach: {total_reach:,}\n"
    msg += f"📊 Total Impressions: {total_impressions:,}\n"

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
