# =============================================================================
# ETF TRACKER — P/E RATIO FETCHER
# =============================================================================
# Uses Alpha Vantage's OVERVIEW endpoint to retrieve the current P/E ratio
# for each equity ETF in PE_WATCHLIST.
#
# Commodity ETFs (AAAU, GLTR, GLD) are deliberately excluded — physical metal
# holders have no earnings, so P/E is not applicable.
#
# ROTATION STRATEGY (Option A):
# Rather than checking all 9 ETFs every day, PE_WATCHLIST is split into 3
# interleaved groups of 3. Each day rotates to the next group based on the
# day-of-year. This keeps the daily request count at 20 (prices) + 3 (P/E) = 23,
# well within Alpha Vantage's free tier of 25/day.
# Each ETF is checked every 3 weekdays — more than frequent enough given that
# P/E is driven by quarterly earnings data and changes slowly.

import requests
import time
import os
from datetime import date
from config import PE_WATCHLIST

# Same API key as the price fetcher — stored as a GitHub Secret
API_KEY = os.environ.get("ALPHA_VANTAGE_KEY", "demo")
BASE_URL = "https://www.alphavantage.co/query"

_TOTAL_GROUPS = 3


def _todays_watchlist() -> tuple[dict, int]:
    """
    Returns (watchlist_subset, group_number) for today's rotation.

    Splits PE_WATCHLIST into 3 interleaved groups using day-of-year % 3:
      Group 1 (indices 0, 3, 6): VOO, DVY, XME
      Group 2 (indices 1, 4, 7): VT,  VDE, EFA
      Group 3 (indices 2, 5, 8): VWO, PHO, QQQ
    """
    all_items = list(PE_WATCHLIST.items())
    group_idx = date.today().timetuple().tm_yday % _TOTAL_GROUPS
    subset = dict(all_items[group_idx::_TOTAL_GROUPS])
    group_num = group_idx + 1
    return subset, group_num


def fetch_pe_ratios():
    """
    Fetches the current P/E ratio for today's rotating group of ETFs
    using Alpha Vantage's OVERVIEW endpoint.

    Returns a tuple of:
      - dict: { "VOO": {"name": "S&P 500", "pe_ratio": 26.5}, "VWO": None, ... }
      - str:  rotation note for the notification (e.g. "Group 2/3 — ...")
    """
    todays_tickers, group_num = _todays_watchlist()
    rotation_note = (
        f"Group {group_num}/{_TOTAL_GROUPS} — rotating daily "
        f"(full cycle every {_TOTAL_GROUPS} weekdays)"
    )

    results = {}

    print(f"P/E rotation: {rotation_note}")
    print(
        f"Today's ETFs: {', '.join(todays_tickers.keys())}  "
        f"(API budget: 20 price + {len(todays_tickers)} P/E = "
        f"{20 + len(todays_tickers)}/25)"
    )
    print(f"\nFetching P/E ratios for {len(todays_tickers)} ETFs via Alpha Vantage...")

    for i, (ticker, name) in enumerate(todays_tickers.items()):
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
        if i < len(todays_tickers) - 1:
            time.sleep(13)

    return results, rotation_note


if __name__ == "__main__":
    ratios, note = fetch_pe_ratios()
    print(f"\nRotation note: {note}")
    print("Raw results:", ratios)
