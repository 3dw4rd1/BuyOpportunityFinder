# =============================================================================
# ETF TRACKER — PRICE FETCHER (Alpha Vantage edition)
# =============================================================================
# Uses the Alpha Vantage API instead of Yahoo Finance.
# Yahoo Finance blocks requests from cloud servers like GitHub Actions.
# Alpha Vantage is a proper, free, official API that works reliably everywhere.
#
# Free tier limit: 25 requests/day — plenty for our 10 ETFs.
# We add a small delay between requests to stay within their rate limits.

import requests
import time
import os
from config import WATCHLIST

# Your Alpha Vantage API key — stored as a GitHub Secret called ALPHA_VANTAGE_KEY
API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "demo")
BASE_URL = "https://www.alphavantage.co/query"

# Alpha Vantage uses a different ticker format for non-US exchanges.
# NZX tickers need the exchange prefix: TWH.NZ → NZE:TWH
def format_ticker_for_alphavantage(ticker: str) -> str:
    if ticker.endswith(".NZ"):
        base = ticker.replace(".NZ", "")
        return f"NZE:{base}"
    return ticker  # US tickers (VDE, PHO, etc.) work as-is


def fetch_prices():
    """
    Fetches the last 2 closing prices for each ticker using Alpha Vantage.

    Returns a dict like:
    {
        "VDE": {"name": "Vanguard Energy Index", "prev_close": 112.34,
                "last_close": 115.67, "currency": "USD"},
        ...
    }
    Returns None for a ticker if it can't be fetched.
    """
    results = {}

    print(f"Fetching prices for {len(WATCHLIST)} ETFs via Alpha Vantage...")

    for i, (ticker, name) in enumerate(WATCHLIST.items()):
        av_ticker = format_ticker_for_alphavantage(ticker)
        currency = "NZD" if ticker.endswith(".NZ") else "USD"

        try:
            params = {
                "function": "TIME_SERIES_DAILY",
                "symbol": av_ticker,
                "outputsize": "compact",  # Only fetches last 100 days — faster
                "apikey": API_KEY,
            }

            response = requests.get(BASE_URL, params=params, timeout=15)
            data = response.json()

            # Check for API errors
            if "Error Message" in data:
                print(f"  ❌  {name} ({ticker}): Ticker not found — {data['Error Message']}")
                results[ticker] = None
                continue

            if "Information" in data:
                # This means we hit the rate limit
                print(f"  ⚠️  Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                # Retry once
                response = requests.get(BASE_URL, params=params, timeout=15)
                data = response.json()

            time_series = data.get("Time Series (Daily)", {})

            if len(time_series) < 2:
                print(f"  ⚠️  {name} ({ticker}): Not enough data returned")
                results[ticker] = None
                continue

            # The time series is a dict keyed by date string — sort to get latest
            sorted_dates = sorted(time_series.keys(), reverse=True)
            last_close = round(float(time_series[sorted_dates[0]]["4. close"]), 4)
            prev_close = round(float(time_series[sorted_dates[1]]["4. close"]), 4)

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

        # Alpha Vantage free tier allows 5 requests/minute.
        # We wait 13 seconds between each request to stay safely under that.
        # (Only pause between requests, not after the last one)
        if i < len(WATCHLIST) - 1:
            time.sleep(13)

    return results


if __name__ == "__main__":
    prices = fetch_prices()
    print("\nRaw results:", prices)
