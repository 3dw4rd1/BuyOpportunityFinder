# =============================================================================
# ETF TRACKER — ANALYSER
# =============================================================================
# Takes the raw price data and works out what moved, by how much,
# and whether it crossed your 3% alert threshold.

from config import ALERT_THRESHOLD_PCT


def analyse(prices: dict):
    """
    Calculates % change for each ETF and categorises the results.

    Returns a dict:
    {
        "movers": [list of ETFs that moved >= threshold, sorted biggest first],
        "all":    [all ETFs with their % change, sorted biggest move first],
        "has_alert": True/False — whether anything hit the threshold
    }

    Each item in the lists looks like:
    {
        "ticker": "VDE",
        "name": "Vanguard Energy Index",
        "prev_close": 112.34,
        "last_close": 115.67,
        "pct_change": +2.96,
        "currency": "USD",
        "direction": "📈" or "📉"
    }
    """
    all_results = []

    for ticker, data in prices.items():
        if data is None:
            # Skip tickers that failed to fetch
            continue

        prev = data["prev_close"]
        last = data["last_close"]

        if prev == 0:
            continue  # Avoid division by zero

        pct_change = round(((last - prev) / prev) * 100, 2)
        direction = "📈" if pct_change >= 0 else "📉"

        all_results.append({
            "ticker": ticker,
            "name": data["name"],
            "prev_close": prev,
            "last_close": last,
            "pct_change": pct_change,
            "currency": data["currency"],
            "direction": direction,
        })

    # Sort all results by absolute % change — biggest movers first
    all_results.sort(key=lambda x: abs(x["pct_change"]), reverse=True)

    # Filter to only those that hit the alert threshold
    movers = [r for r in all_results if abs(r["pct_change"]) >= ALERT_THRESHOLD_PCT]

    return {
        "movers": movers,
        "all": all_results,
        "has_alert": len(movers) > 0,
    }


if __name__ == "__main__":
    # Quick test with dummy data
    dummy = {
        "VDE": {"name": "Vanguard Energy", "prev_close": 100.0, "last_close": 104.5, "currency": "USD"},
        "GLD.NZ": {"name": "SmartShares Gold", "prev_close": 10.0, "last_close": 9.6, "currency": "NZD"},
    }
    result = analyse(dummy)
    print("Movers:", result["movers"])
    print("Has alert:", result["has_alert"])
