# =============================================================================
# ETF TRACKER — NOTIFIER
# =============================================================================
# Formats the analysis results into a clean message and sends it
# to your phone via Ntfy (ntfy.sh).

import requests
from datetime import date
from config import NTFY_URL, ALERT_THRESHOLD_PCT, PE_ALERT_THRESHOLD


def format_message(analysis: dict) -> tuple[str, str]:
    """
    Formats the analysis into a notification title and body.

    Returns: (title, body) as strings
    """
    movers = analysis["movers"]
    today = date.today().strftime("%d %b %Y")

    # --- Title ---
    gains = [m for m in movers if m["pct_change"] > 0]
    losses = [m for m in movers if m["pct_change"] < 0]

    title_parts = []
    if gains:
        title_parts.append(f"{len(gains)} up")
    if losses:
        title_parts.append(f"{len(losses)} down")

    title = f"ETF Alert {today} - " + ", ".join(title_parts)

    # --- Body ---
    lines = [f"Moves >= {ALERT_THRESHOLD_PCT}% detected:\n"]

    for m in movers:
        sign = "+" if m["pct_change"] > 0 else ""
        lines.append(
            f"{m['direction']} {m['name']}\n"
            f"   {m['currency']} {m['prev_close']} → {m['last_close']} "
            f"({sign}{m['pct_change']}%)\n"
        )

    body = "\n".join(lines)
    return title, body


def send_notification(analysis: dict) -> bool:
    """
    Sends a push notification to Ntfy if there are any movers.
    Returns True if sent successfully, False otherwise.
    """
    if not analysis["has_alert"]:
        print("No ETFs moved more than the threshold today. No notification sent.")
        return False

    title, body = format_message(analysis)

    print(f"\n--- Notification Preview ---")
    print(f"Title: {title}")
    print(f"Body:\n{body}")
    print(f"----------------------------\n")

    try:
        response = requests.post(
            NTFY_URL,
            data=body.encode("utf-8"),
            headers={
                "Title": title,
                "Priority": "high",
                "Tags": "chart_with_upwards_trend,money",
            },
        )

        if response.ok:
            print(f"✅ Notification sent successfully to {NTFY_URL}")
            return True
        else:
            print(f"❌ Ntfy returned status {response.status_code}: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send notification: {e}")
        return False


def send_pe_notification(pe_analysis: dict) -> bool:
    """
    Sends a push notification with the daily P/E ratio status for all tracked ETFs.
    ETFs above the threshold are flagged as expensive; below as potential buys.
    Returns True if sent successfully, False otherwise.
    """
    if not pe_analysis["has_alert"]:
        print("No P/E data available. No notification sent.")
        return False

    today = date.today().strftime("%d %b %Y")
    above = pe_analysis["above"]
    below = pe_analysis["below"]
    skipped = pe_analysis["skipped"]

    # --- Title ---
    parts = []
    if above:
        parts.append(f"{len(above)} above")
    if below:
        parts.append(f"{len(below)} below")
    title = f"P/E Alert {today} — " + ", ".join(parts) + f" ({PE_ALERT_THRESHOLD})"

    # --- Body ---
    lines = [f"P/E threshold: {PE_ALERT_THRESHOLD}\n"]

    if above:
        lines.append("🔴 Above threshold (expensive):")
        for m in above:
            lines.append(f"   {m['name']} ({m['ticker']}): {m['pe_ratio']}")
        lines.append("")

    if below:
        lines.append("🟢 Below threshold (potential buy):")
        for m in below:
            lines.append(f"   {m['name']} ({m['ticker']}): {m['pe_ratio']}")
        lines.append("")

    if skipped:
        lines.append(f"⚪ No P/E data: {', '.join(skipped)}")

    note = pe_analysis.get("note")
    if note:
        lines.append(f"\n({note})")

    body = "\n".join(lines)

    print(f"\n--- P/E Notification Preview ---")
    print(f"Title: {title}")
    print(f"Body:\n{body}")
    print(f"--------------------------------\n")

    try:
        response = requests.post(
            NTFY_URL,
            data=body.encode("utf-8"),
            headers={
                "Title": title,
                "Priority": "default",
                "Tags": "bar_chart,moneybag",
            },
        )

        if response.ok:
            print(f"✅ P/E notification sent successfully to {NTFY_URL}")
            return True
        else:
            print(f"❌ Ntfy returned status {response.status_code}: {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send P/E notification: {e}")
        return False


if __name__ == "__main__":
    # Quick test — simulates what a real notification would look like
    dummy_analysis = {
        "has_alert": True,
        "movers": [
            {"ticker": "VDE", "name": "Vanguard Energy Index", "prev_close": 100.0,
             "last_close": 104.5, "pct_change": 4.5, "currency": "USD", "direction": "📈"},
            {"ticker": "GLD.NZ", "name": "SmartShares Gold ETF", "prev_close": 10.0,
             "last_close": 9.55, "pct_change": -4.5, "currency": "NZD", "direction": "📉"},
        ],
        "all": []
    }
    send_notification(dummy_analysis)
