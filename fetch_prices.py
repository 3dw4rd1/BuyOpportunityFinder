# =============================================================================
# ETF TRACKER — PRICE FETCHER
# =============================================================================
# This file pulls the two most recent closing prices for each ETF in your
# watchlist using Yahoo Finance (free, no API key needed).

import yfinance as yf
from config import WATCHLIST


def fetch_prices():
    """
    Fetches the last 2 closing prices for each ticker in the watchlist.

    Returns a dict like:
    {
        "VDE": {"prev_close": 112.34, "last_close": 115.67, "currency": "USD"},
        ...
    }
    Returns an empty dict entry if a ticker can't be fetched.
    """
    results = {}

    print(f"Fetching prices for {len(WATCHLIST)} ETFs...")

    for ticker, name in WATCHLIST.items():
        try:
            data = yf.Ticker(ticker)
            # Fetch last 5 days of data to ensure we always get at least 2
            # trading days (weekends/holidays can create gaps)
            hist = data.history(period="5d")

            if len(hist) < 2:
                print(f"  ⚠️  {name} ({ticker}): Not enough data returned")
                results[ticker] = None
                continue

            # The last row is the most recent close, second-to-last is previous
            last_close = round(hist["Close"].iloc[-1], 4)
            prev_close = round(hist["Close"].iloc[-2], 4)

            # Try to get currency from the ticker info
            try:
                currency = data.info.get("currency", "?")
            except Exception:
                currency = "NZD" if ticker.endswith(".NZ") else "USD"

            results[ticker] = {
                "name": name,
                "prev_close": prev_close,
                "last_close": last_close,
                "currency": currency,
            }
            print(f"  ✅  {name} ({ticker}): {prev_close} → {last_close} {currency}")

        except Exception as e:
            print(f"  ❌  {name} ({ticker}): Failed — {e}")
            results[ticker] = None

    return results


if __name__ == "__main__":
    # If you run this file directly, it'll just print the prices — useful for testing
    prices = fetch_prices()
    print("\nRaw results:", prices)
