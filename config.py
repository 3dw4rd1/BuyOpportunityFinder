# =============================================================================
# ETF TRACKER — CONFIGURATION
# =============================================================================
# This is the main settings file. Edit this to change your watchlist,
# notification threshold, or timing preferences.

import os

# --- Your Ntfy topic name ---
# This is pulled from an environment variable (a GitHub Secret) so your
# topic name is never visible in your code. You'll set this up in GitHub.
NTFY_TOPIC = os.environ.get("NTFY_TOPIC", "your-topic-name-here")
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"

# --- Alert threshold ---
# A notification will only be sent if at least one ETF moves by this amount.
ALERT_THRESHOLD_PCT = 3.0

# --- Your ETF watchlist ---
# Format: "TICKER": "Friendly name you want to see in notifications"
WATCHLIST = {
    # US-listed ETFs (NYSE Arca)
    "VDE":  "Vanguard Energy Index",
    "PHO":  "Invesco Water Resources",
    "AAAU": "Goldman Sachs Physical Gold",
    "GLTR": "Aberdeen Physical Precious Metals",

    # NZX-listed SmartShares ETFs
    "TWH.NZ": "SmartShares Total World (NZD Hedged)",
    "EMF.NZ": "SmartShares Emerging Markets",
    "ASR.NZ": "SmartShares Australian Resources",
    "ASD.NZ": "SmartShares Australian Dividend",
    "USF.NZ": "SmartShares US500",
    "GLD.NZ": "SmartShares Gold ETF",
}
