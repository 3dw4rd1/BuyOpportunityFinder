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
# 20 ETFs rotated in groups of 3 by day-of-year. P/E data sourced from Yahoo Finance.
PE_WATCHLIST = {
    "VOO":  "S&P 500",
    "VT":   "Vanguard Total World",
    "VUG":  "Vanguard Growth ETF",
    "QQQ":  "Invesco Nasdaq-100",
    "VWO":  "Vanguard Emerging Markets",
    "EFA":  "iShares MSCI EAFE (Developed ex-US)",
    "EWA":  "iShares MSCI Australia",
    "EWJ":  "iShares MSCI Japan",
    "EZU":  "iShares MSCI Eurozone",
    "INDA": "iShares MSCI India",
    "FXI":  "iShares China Large-Cap",
    "VDE":  "Vanguard Energy Index",
    "PHO":  "Invesco Water Resources",
    "DVY":  "iShares Dividend Select",
    "XME":  "SPDR Metals & Mining",
    "VNQ":  "Vanguard Real Estate ETF",
    "IYH":  "iShares US Healthcare ETF",
    "XLF":  "Financial Select SPDR",
    "XLI":  "Industrial Select SPDR",
    "XLY":  "Consumer Discretionary Select SPDR",
}

# --- Your ETF watchlist ---
# Format: "TICKER": "Friendly name you want to see in notifications"
#
# NOTE ON NZX FUNDS: Alpha Vantage (our free data source) doesn't support
# NZX tickers. Instead we track the underlying US ETFs that the SmartShares
# funds invest in — the % price moves are essentially identical, which is
# all we need for buy/sell signals.
WATCHLIST = {
    "VDE":  "Vanguard Energy Index",
    "PHO":  "Invesco Water Resources",
    "AAAU": "Goldman Sachs Physical Gold",
    "GLTR": "Aberdeen Physical Precious Metals",
    "VT":   "SmartShares Total World [via VT]",
    "VWO":  "SmartShares Emerging Markets [via VWO]",
    "VOO":  "SmartShares US500 [via VOO]",
    "GLD":  "SmartShares Gold ETF [via GLD]",
    "XME":  "SmartShares AU Resources [via XME]",
    "DVY":  "SmartShares AU Dividend [via DVY]",
    "VUG":  "Vanguard Growth ETF",
    "SOXX": "iShares Semiconductor ETF",
    "ARKK": "ARK Innovation ETF",
    "XBI":  "SPDR S&P Biotech ETF",
    "EWA":  "iShares MSCI Australia",
    "VEA":  "Vanguard FTSE Developed Markets",
    "EWJ":  "iShares MSCI Japan",
    "EZU":  "iShares MSCI Eurozone",
    "FXI":  "iShares China Large-Cap",
    "INDA": "iShares MSCI India",
    "VNQ":  "Vanguard Real Estate ETF",
    "TLT":  "iShares 20+ Year Treasury",
    "WOOD": "iShares Global Timber & Forestry",
    "IYH":  "iShares US Healthcare ETF",
    "XLY":  "Consumer Discretionary Select SPDR",
}
