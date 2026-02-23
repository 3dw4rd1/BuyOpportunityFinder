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
ALERT_THRESHOLD_PCT = 4.0

# --- P/E ratio alert threshold ---
# A notification is sent daily showing which ETFs are above or below this value.
# Above = potentially expensive, below = potential buy opportunity.
PE_ALERT_THRESHOLD = 23.0

# --- P/E watchlist ---
# Matches the 10 ETFs in WATCHLIST. P/E data is sourced from Yahoo Finance.
# Commodity ETFs (AAAU, GLTR, GLD) have no earnings and will be reported as
# skipped — Yahoo Finance returns no trailing P/E for physical metal holders.
PE_WATCHLIST = {
    "VDE":  "Vanguard Energy Index",
    "PHO":  "Invesco Water Resources",
    "AAAU": "Goldman Sachs Physical Gold",        # commodity — no P/E
    "GLTR": "Aberdeen Physical Precious Metals",  # commodity — no P/E
    "VT":   "Vanguard Total World",
    "VWO":  "Vanguard Emerging Markets",
    "VOO":  "S&P 500",
    "GLD":  "SPDR Gold Shares",                   # commodity — no P/E
    "XME":  "SPDR Metals & Mining",
    "DVY":  "iShares Dividend Select",
}

# --- Your ETF watchlist ---
# Format: "TICKER": "Friendly name you want to see in notifications"
#
# NOTE ON NZX FUNDS: Alpha Vantage (our free data source) doesn't support
# NZX tickers. Instead we track the underlying US ETFs that the SmartShares
# funds invest in — the % price moves are essentially identical, which is
# all we need for buy/sell signals.
WATCHLIST = {
    # Your original US-listed picks
    "VDE":  "Vanguard Energy Index",
    "PHO":  "Invesco Water Resources",
    "AAAU": "Goldman Sachs Physical Gold",
    "GLTR": "Aberdeen Physical Precious Metals",

    # SmartShares NZX funds tracked via their underlying US ETF equivalents:
    "VT":   "SmartShares Total World [via VT]",       # TWH tracks Vanguard Total World (VT)
    "VWO":  "SmartShares Emerging Markets [via VWO]", # EMF tracks Vanguard FTSE Emerging Markets (VWO)
    "VOO":  "SmartShares US500 [via VOO]",            # USF tracks Vanguard S&P 500 (VOO)
    "GLD":  "SmartShares Gold ETF [via GLD]",         # GLD.NZ tracks gold price, same as SPDR GLD

    # Australian funds — tracked via US-listed proxies (ASX not supported on free tier)
    "XME":  "SmartShares AU Resources [via XME]",  # SPDR Metals & Mining ETF — closely tracks ASX resources
    "DVY":  "SmartShares AU Dividend [via DVY]",   # iShares Dividend Select ETF — similar dividend focus
}
