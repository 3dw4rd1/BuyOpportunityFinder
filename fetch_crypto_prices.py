# =============================================================================
# CRYPTO TRACKER — PRICE FETCHER (CoinGecko edition)
# =============================================================================
# Uses the CoinGecko public API — no API key required.
# Fetches current price and 24-hour percentage change for each coin in one
# request, then reconstructs the "previous price" from those two values so the
# rest of the pipeline (analyse / notify) works identically to the ETF tracker.
#
# CoinGecko free tier: 10–30 calls/min — well within budget for 1 call/day.

import requests
from config import CRYPTO_WATCHLIST

BASE_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_crypto_prices():
    """
    Fetches current price and 24-hour change for each coin via CoinGecko.

    Returns a dict like:
    {
        "bitcoin":  {"name": "Bitcoin (BTC)",  "prev_close": 94200.00,
                     "last_close": 97500.00,   "currency": "USD"},
        ...
    }
    Returns None for a coin if it can't be fetched.
    """
    ids = ",".join(CRYPTO_WATCHLIST.keys())

    print(f"Fetching crypto prices for {len(CRYPTO_WATCHLIST)} coins via CoinGecko...")

    try:
        params = {
            "ids": ids,
            "vs_currencies": "usd",
            "include_24hr_change": "true",
        }

        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException as e:
        print(f"  ❌  CoinGecko request failed: {e}")
        return {coin_id: None for coin_id in CRYPTO_WATCHLIST}

    results = {}

    for coin_id, name in CRYPTO_WATCHLIST.items():
        coin_data = data.get(coin_id)

        if not coin_data:
            print(f"  ❌  {name}: No data returned from CoinGecko")
            results[coin_id] = None
            continue

        last_close = coin_data.get("usd")
        pct_change_24h = coin_data.get("usd_24h_change")

        if last_close is None or pct_change_24h is None:
            print(f"  ❌  {name}: Missing price or 24h-change field")
            results[coin_id] = None
            continue

        # Back-calculate what the price was 24 hours ago
        prev_close = round(last_close / (1 + pct_change_24h / 100), 6)
        last_close = round(last_close, 6)

        results[coin_id] = {
            "name": name,
            "prev_close": prev_close,
            "last_close": last_close,
            "currency": "USD",
        }

        sign = "+" if pct_change_24h >= 0 else ""
        print(f"  ✅  {name}: ${prev_close:,.2f} → ${last_close:,.2f} "
              f"({sign}{pct_change_24h:.2f}%)")

    return results


if __name__ == "__main__":
    prices = fetch_crypto_prices()
    print("\nRaw results:", prices)
