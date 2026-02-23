# =============================================================================
# ETF TRACKER — P/E RATIO FETCHER
# =============================================================================
# Uses Yahoo Finance (via yfinance) to retrieve the current trailing P/E ratio
# for each ETF in PE_WATCHLIST.
#
# All 10 ETFs are checked every day. Commodity ETFs (AAAU, GLTR, GLD) do not
# have earnings, so Yahoo Finance returns no P/E for them — they are logged as
# skipped rather than treated as errors.

import yfinance as yf
import time
from config import PE_WATCHLIST


def fetch_pe_ratios():
    """
    Fetches the current trailing P/E ratio for every ETF in PE_WATCHLIST
    using Yahoo Finance.

    Returns a tuple of:
      - dict: { "VOO": {"name": "S&P 500", "pe_ratio": 26.5}, "AAAU": None, ... }
      - str:  data-source note for the notification
    """
    note = f"All {len(PE_WATCHLIST)} ETFs checked daily via Yahoo Finance"
    results = {}

    print(f"Fetching P/E ratios for {len(PE_WATCHLIST)} ETFs via Yahoo Finance...")

    for i, (ticker, name) in enumerate(PE_WATCHLIST.items()):
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
        if i < len(PE_WATCHLIST) - 1:
            time.sleep(1)

    return results, note


if __name__ == "__main__":
    ratios, note = fetch_pe_ratios()
    print(f"\nNote: {note}")
    print("Raw results:", ratios)
