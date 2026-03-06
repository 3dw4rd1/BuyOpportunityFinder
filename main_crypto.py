# =============================================================================
# CRYPTO TRACKER — MAIN
# =============================================================================
# Entry point for the crypto price alert system.
# Ties together fetching, analysis, and notification in sequence.

from fetch_crypto_prices import fetch_crypto_prices
from analyse_crypto import analyse_crypto
from notify import send_crypto_notification


def main():
    print("=" * 50)
    print("  CRYPTO TRACKER — 24h Report")
    print("=" * 50)

    # Step 1: Fetch latest prices from CoinGecko
    print("\n[1/3] Fetching prices...")
    prices = fetch_crypto_prices()

    # Step 2: Analyse the price changes
    print("\n[2/3] Analysing movements...")
    analysis = analyse_crypto(prices)

    total = len(analysis["all"])
    movers = len(analysis["movers"])
    print(f"  Tracked {total} coins — {movers} moved ≥ threshold")

    if analysis["all"]:
        print("\n  Full leaderboard:")
        for coin in analysis["all"]:
            sign = "+" if coin["pct_change"] > 0 else ""
            print(f"    {coin['direction']}  {coin['name']:30s}  {sign}{coin['pct_change']}%")

    # Step 3: Send notification if anything hit the threshold
    print("\n[3/3] Sending notification...")
    send_crypto_notification(analysis)

    print("\nDone. ✅")


if __name__ == "__main__":
    main()
