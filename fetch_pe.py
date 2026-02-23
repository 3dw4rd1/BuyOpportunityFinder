# =============================================================================
# ETF TRACKER — P/E RATIO FETCHER
# =============================================================================
# Uses EODHD's Fundamentals API to retrieve the current trailing P/E ratio
# for each equity ETF in PE_WATCHLIST.
#
# All 9 ETFs are checked every day — no rotation required because EODHD
# does not impose the same tight daily request caps as Alpha Vantage's
# free tier.
#
# Commodity ETFs (AAAU, GLTR, GLD) are deliberately excluded — physical metal
# holders have no earnings, so P/E is not applicable.

import requests
import time
import os
from config import PE_WATCHLIST

API_KEY = os.environ.get("EODHD_API_KEY", "demo")
BASE_URL = "https://eodhd.com/api/fundamentals"


def fetch_pe_ratios():
    """
    Fetches the current trailing P/E ratio for every ETF in PE_WATCHLIST
    using the EODHD Fundamentals API.

    Returns a tuple of:
      - dict: { "VOO": {"name": "S&P 500", "pe_ratio": 26.5}, "VWO": None, ... }
      - str:  data-source note for the notification
    """
    note = f"All {len(PE_WATCHLIST)} ETFs checked daily via EODHD Fundamentals API"
    results = {}

    print(f"Fetching P/E ratios for {len(PE_WATCHLIST)} ETFs via EODHD...")

    for i, (ticker, name) in enumerate(PE_WATCHLIST.items()):
        eodhd_ticker = f"{ticker}.US"
        url = f"{BASE_URL}/{eodhd_ticker}"

        try:
            response = requests.get(
                url,
                params={"api_token": API_KEY, "fmt": "json"},
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()

            # EODHD returns an empty dict or error message when the ticker is unknown
            if not data or "General" not in data:
                print(f"  ❌  {name} ({ticker}): No data returned by EODHD")
                results[ticker] = None
                continue

            valuation = data.get("Valuation", {})
            pe_raw = valuation.get("TrailingPE")

            # EODHD uses None, "N/A", 0, or "" when the field isn't available
            if pe_raw is None or pe_raw in ("N/A", "", "0", 0):
                print(f"  ⚠️  {name} ({ticker}): Trailing P/E not available")
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

        except requests.exceptions.HTTPError as e:
            print(f"  ❌  {name} ({ticker}): HTTP error — {e}")
            results[ticker] = None

        except Exception as e:
            print(f"  ❌  {name} ({ticker}): Failed — {e}")
            results[ticker] = None

        # Small delay between requests to be a good API citizen
        if i < len(PE_WATCHLIST) - 1:
            time.sleep(1)

    return results, note


if __name__ == "__main__":
    ratios, note = fetch_pe_ratios()
    print(f"\nNote: {note}")
    print("Raw results:", ratios)
