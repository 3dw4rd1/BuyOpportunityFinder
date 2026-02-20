# =============================================================================
# ETF TRACKER — P/E RATIO FETCHER
# =============================================================================
# Uses Alpha Vantage's OVERVIEW endpoint to retrieve the current P/E ratio
# for each equity ETF in PE_WATCHLIST.
#
# Commodity ETFs (AAAU, GLTR, GLD) are deliberately excluded — physical metal
# holders have no earnings, so P/E is not applicable.

import requests
import time
import os
from config import PE_WATCHLIST

# Same API key as the price fetcher — stored as a GitHub Secret
API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "demo")
BASE_URL = "https://www.alphavantage.co/query"


def fetch_pe_ratios():
    """
    Fetches the current P/E ratio for each ticker in PE_WATCHLIST
    using Alpha Vantage's OVERVIEW endpoint.

    Returns a dict like:
    {
        "VOO": {"name": "S&P 500", "pe_ratio": 26.5},
        "VWO": None,   # if P/E data wasn't available
        ...
    }
    """
    results = {}

    print(f"Fetching P/E ratios for {len(PE_WATCHLIST)} ETFs via Alpha Vantage...")

    for i, (ticker, name) in enumerate(PE_WATCHLIST.items()):
        try:
            params = {
                "function": "OVERVIEW",
                "symbol": ticker,
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
                # Rate limit hit — wait and retry once
                print(f"  ⚠️  Rate limit hit. Waiting 60 seconds...")
                time.sleep(60)
                response = requests.get(BASE_URL, params=params, timeout=15)
                data = response.json()
                if "Information" in data or "Error Message" in data:
                    print(f"  ❌  {name} ({ticker}): Still rate limited after retry — skipping")
                    results[ticker] = None
                    continue

            pe_raw = data.get("PERatio", "None")

            # Alpha Vantage returns "None" (string) when the field isn't available
            if not pe_raw or pe_raw in ("None", "-", "0"):
                print(f"  ⚠️  {name} ({ticker}): P/E ratio not available")
                results[ticker] = None
                continue

            pe_ratio = round(float(pe_raw), 2)
            results[ticker] = {
                "name": name,
                "pe_ratio": pe_ratio,
            }
            print(f"  ✅  {name} ({ticker}): P/E = {pe_ratio}")

        except (ValueError, TypeError) as e:
            print(f"  ⚠️  {name} ({ticker}): Could not parse P/E ratio — {e}")
            results[ticker] = None

        except Exception as e:
            print(f"  ❌  {name} ({ticker}): Failed — {e}")
            results[ticker] = None

        # Alpha Vantage free tier: 5 requests/minute — 13s delay keeps us safe
        if i < len(PE_WATCHLIST) - 1:
            time.sleep(13)

    return results


if __name__ == "__main__":
    ratios = fetch_pe_ratios()
    print("\nRaw results:", ratios)
