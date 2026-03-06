# =============================================================================
# CRYPTO TRACKER — ANALYSER
# =============================================================================
# Takes the raw crypto price data and works out what moved, by how much,
# and whether it crossed the alert threshold.
# Mirrors analyse.py but uses CRYPTO_ALERT_THRESHOLD_PCT.

from config import CRYPTO_ALERT_THRESHOLD_PCT


def analyse_crypto(prices: dict):
    """
    Calculates % change for each coin and categorises the results.

    Returns a dict:
    {
        "movers": [list of coins that moved >= threshold, sorted biggest first],
        "all":    [all coins with their % change, sorted biggest move first],
        "has_alert": True/False — whether anything hit the threshold
    }

    Each item in the lists looks like:
    {
        "ticker": "bitcoin",
        "name": "Bitcoin (BTC)",
        "prev_close": 94200.00,
        "last_close": 97500.00,
        "pct_change": +3.51,
        "currency": "USD",
        "direction": "📈" or "📉"
    }
    """
    all_results = []

    for coin_id, data in prices.items():
        if data is None:
            continue

        prev = data["prev_close"]
        last = data["last_close"]

        if prev == 0:
            continue

        pct_change = round(((last - prev) / prev) * 100, 2)
        direction = "📈" if pct_change >= 0 else "📉"

        all_results.append({
            "ticker": coin_id,
            "name": data["name"],
            "prev_close": prev,
            "last_close": last,
            "pct_change": pct_change,
            "currency": data["currency"],
            "direction": direction,
        })

    # Sort by absolute % change — biggest movers first
    all_results.sort(key=lambda x: abs(x["pct_change"]), reverse=True)

    # Filter to only those that hit the alert threshold
    movers = [r for r in all_results if abs(r["pct_change"]) >= CRYPTO_ALERT_THRESHOLD_PCT]

    return {
        "movers": movers,
        "all": all_results,
        "has_alert": len(movers) > 0,
    }


if __name__ == "__main__":
    dummy = {
        "bitcoin":  {"name": "Bitcoin (BTC)",  "prev_close": 94000.0, "last_close": 99000.0, "currency": "USD"},
        "ethereum": {"name": "Ethereum (ETH)", "prev_close": 3000.0,  "last_close": 2850.0,  "currency": "USD"},
        "dogecoin": {"name": "Dogecoin (DOGE)","prev_close": 0.20,    "last_close": 0.204,   "currency": "USD"},
    }
    result = analyse_crypto(dummy)
    print("Movers:", result["movers"])
    print("Has alert:", result["has_alert"])
