def format_report(data, balance, spend_cap, amount_spent, remaining):
    text = f"📊 META ADS REPORT HARI INI\n\n"
    text += f"🏢 Account: {AD_ACCOUNT_ID}\n"
    text += f"💰 Saldo: {format_rp(balance)}\n\n"

    # 🔥 SPENDING LIMIT INFO
    if spend_cap and float(spend_cap) > 0:
        text += f"🚧 Account Spending Limit\n"
        text += f"Remaining: {format_rp(remaining)}\n"
        text += f"Spent: {format_rp(amount_spent)}\n"
        text += f"Limit: {format_rp(spend_cap)}\n\n"

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

            # 🔥 SAFE FUNCTION CALL
            purchase = get_purchase(item.get("actions") or [])
            purchase_value = get_purchase_value(item.get("action_values") or [])
            roas = get_roas(item) if spend > 0 else 0

        except Exception as e:
            print("ERROR PARSING ITEM:", e)
            continue

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

    # 🔥 SAFE TOTAL ROAS
    total_roas = total_revenue / total_spend if total_spend > 0 else 0

    text += f"========== TOTAL ==========\n"
    text += f"Spend: {format_rp(total_spend)}\n"
    text += f"Purchase: {int(total_purchase)}\n"
    text += f"Revenue: {format_rp(total_revenue)}\n"
    text += f"ROAS: {total_roas:.2f}\n"

    return text
