# =============================================================================
# ETF TRACKER — MAIN
# =============================================================================
# This is the file you run (or GitHub Actions runs for you).
# It ties together fetching, analysis, and notification in sequence.

from fetch_prices import fetch_prices
from analyse import analyse
from notify import send_notification


def main():
    print("=" * 50)
    print("  ETF TRACKER — Daily Report")
    print("=" * 50)

    # Step 1: Fetch latest prices from Alpha Vantage
    print("\n[1/3] Fetching prices...")
    prices = fetch_prices()

    # Step 2: Analyse the price changes
    print("\n[2/3] Analysing movements...")
    analysis = analyse(prices)

    total = len(analysis["all"])
    movers = len(analysis["movers"])
    print(f"  Tracked {total} ETFs — {movers} moved ≥ threshold")

    if analysis["all"]:
        print("\n  Full leaderboard:")
        for etf in analysis["all"]:
            sign = "+" if etf["pct_change"] > 0 else ""
            print(f"    {etf['direction']}  {etf['name']:40s}  {sign}{etf['pct_change']}%")

    # Step 3: Send notification if anything hit the threshold
    print("\n[3/3] Sending notification...")
    send_notification(analysis)

    print("\nDone. ✅")


if __name__ == "__main__":
    main()
