# =============================================================================
# ETF TRACKER — P/E RATIO ANALYSER
# =============================================================================
# Takes the raw P/E data and classifies each ETF as above or below the
# alert threshold. ETFs where P/E data wasn't available are tracked separately
# so the notification can report them as skipped rather than silently dropped.

from config import PE_ALERT_THRESHOLD


def analyse_pe(pe_data: dict):
    """
    Compares each ETF's P/E ratio against PE_ALERT_THRESHOLD.

    Returns a dict:
    {
        "above":   [ETFs with P/E > threshold, sorted highest first],
        "below":   [ETFs with P/E < threshold, sorted lowest first],
        "all":     [all ETFs with P/E data, sorted highest to lowest],
        "skipped": [ticker strings where P/E data was unavailable],
        "has_alert": True if any P/E data was retrieved, False otherwise
    }

    Each item in above/below/all looks like:
    {
        "ticker":   "VOO",
        "name":     "S&P 500",
        "pe_ratio": 26.5,
        "is_above": True,
        "direction": "🔴"   # 🔴 = above threshold, 🟢 = below threshold
    }
    """
    above = []
    below = []
    all_results = []
    skipped = []

    for ticker, data in pe_data.items():
        if data is None:
            skipped.append(ticker)
            continue

        pe = data["pe_ratio"]
        is_above = pe > PE_ALERT_THRESHOLD

        entry = {
            "ticker": ticker,
            "name": data["name"],
            "pe_ratio": pe,
            "is_above": is_above,
            "direction": "🔴" if is_above else "🟢",
        }

        all_results.append(entry)
        if is_above:
            above.append(entry)
        else:
            below.append(entry)

    return {
        "above":     sorted(above, key=lambda x: x["pe_ratio"], reverse=True),
        "below":     sorted(below, key=lambda x: x["pe_ratio"]),
        "all":       sorted(all_results, key=lambda x: x["pe_ratio"], reverse=True),
        "skipped":   skipped,
        "has_alert": len(all_results) > 0,
    }


if __name__ == "__main__":
    # Quick test with dummy data
    dummy = {
        "VOO": {"name": "S&P 500",               "pe_ratio": 26.5},
        "QQQ": {"name": "Invesco Nasdaq-100",     "pe_ratio": 34.1},
        "VWO": {"name": "Vanguard Emerging Mkts", "pe_ratio": 14.2},
        "EFA": {"name": "iShares MSCI EAFE",      "pe_ratio": 15.8},
        "GLD": None,  # commodity, no P/E
    }
    result = analyse_pe(dummy)
    print(f"Above threshold ({PE_ALERT_THRESHOLD}):", [(e["ticker"], e["pe_ratio"]) for e in result["above"]])
    print(f"Below threshold ({PE_ALERT_THRESHOLD}):", [(e["ticker"], e["pe_ratio"]) for e in result["below"]])
    print("Skipped:", result["skipped"])
    print("Has alert:", result["has_alert"])
