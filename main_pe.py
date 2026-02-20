# =============================================================================
# ETF TRACKER — P/E RATIO REPORT (entry point)
# =============================================================================
# Run this file to fetch P/E ratios, analyse them against the threshold,
# and send a push notification summarising the results.
#
# This is separate from main.py (which handles price % change alerts) so
# P/E checks can run on their own schedule — once daily rather than twice.

from fetch_pe import fetch_pe_ratios
from analyse_pe import analyse_pe
from notify import send_pe_notification


def main():
    print("=" * 50)
    print("  ETF TRACKER — P/E Ratio Report")
    print("=" * 50)

    # Step 1: Fetch P/E ratios for today's rotation group
    print("\n[1/3] Fetching P/E ratios...")
    pe_data, rotation_note = fetch_pe_ratios()

    # Step 2: Classify each ETF as above or below the threshold
    print("\n[2/3] Analysing P/E ratios...")
    pe_analysis = analyse_pe(pe_data)
    pe_analysis["note"] = rotation_note  # passed through to the notification

    tracked = len(pe_analysis["all"])
    skipped = len(pe_analysis["skipped"])
    above = len(pe_analysis["above"])
    below = len(pe_analysis["below"])
    print(f"  Retrieved P/E for {tracked} ETFs ({skipped} skipped — no data available)")
    print(f"  {above} above threshold, {below} below threshold")

    if pe_analysis["all"]:
        print("\n  P/E leaderboard:")
        for etf in pe_analysis["all"]:
            marker = "▲" if etf["is_above"] else "▼"
            print(f"    {etf['direction']} {marker}  {etf['name']:40s}  P/E {etf['pe_ratio']}")

    # Step 3: Send notification
    print("\n[3/3] Sending P/E notification...")
    send_pe_notification(pe_analysis)

    print("\nDone. ✅")


if __name__ == "__main__":
    main()
