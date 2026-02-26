# =============================================================================
# ETF TRACKER — P/E RATIO FETCHER
# =============================================================================
# Uses Yahoo Finance (via yfinance) to retrieve the current trailing P/E ratio
# for a rotating group of ETFs from PE_WATCHLIST.
#
# 20 ETFs are rotated in groups of 3 by day-of-year to stay within API limits.

import yfinance as yf
import time
from datetime import date
from config import PE_WATCHLIST


def fetch_pe_ratios():
    """
    Fetches the current trailing P/E ratio for a rotating group of ETFs
    from PE_WATCHLIST using Yahoo Finance.

    Returns a tuple of:
      - dict: { "VOO": {"name": "S&P 500", "pe_ratio": 26.5}, ... }
      - str:  data-source note for the notification
    """
    tickers = list(PE_WATCHLIST.items())
    total = len(tickers)
    group_size = 3

    day_index = date.today().timetuple().tm_yday
    start = (day_index * group_size) % total
    group = tickers[start:start + group_size]

    # Handle wrap-around if group crosses end of list
    if len(group) < group_size:
        group += tickers[:group_size - len(group)]

    note = (
        f"Showing {group_size} of {total} ETFs "
        f"(rotation {start // group_size + 1} of {-(-total // group_size)}) "
        f"— full cycle every ~{-(-total // group_size)} weekdays"
    )

    results = {}

    print(f"Fetching P/E ratios for {group_size} of {total} ETFs via Yahoo Finance...")

    for i, (ticker, name) in enumerate(group):
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            pe_raw = info.get("trailingPE")

            if pe_raw is None or pe_raw == 0:
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

        except Exception as e:
            print(f"  ❌  {name} ({ticker}): Failed — {e}")
            results[ticker] = None

        # Small delay between requests to avoid rate limiting
        if i < len(group) - 1:
            time.sleep(1)

    return results, note


if __name__ == "__main__":
    ratios, note = fetch_pe_ratios()
    print(f"\nNote: {note}")
    print("Raw results:", ratios)
