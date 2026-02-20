# ETF Tracker — Daily Buy Opportunity Notifier

Automatically checks your ETF watchlist twice a day and sends a push notification
to your phone (via Ntfy) if anything moves 4% or more. Also sends a daily P/E
ratio report to flag potentially expensive or undervalued ETFs.

Runs entirely for free on GitHub Actions — no server needed.

---

## How it works

Two separate pipelines run every weekday:

**Price tracker** (runs twice daily):
1. GitHub Actions triggers the script automatically
2. It fetches the latest closing prices for all 10 ETFs via Alpha Vantage
3. It compares each price to the previous day's close
4. If anything moved ≥ 4%, you get a push notification on your phone
5. On quiet days, nothing is sent

**P/E ratio tracker** (runs once daily):
1. Fetches P/E ratios for a rotating group of 3 ETFs from the 9-ETF P/E watchlist
2. Flags ETFs above 23.0 as potentially expensive, below as potential buy opportunities
3. Sends a daily summary notification (always fires if data is returned)
4. The full 9-ETF watchlist cycles through every 3 weekdays to stay within API limits

---

## Schedule (Melbourne time)

All times are approximate — GitHub Actions can run up to ~15 minutes late.
Note the day offset: because the morning runs are early UTC, they arrive in Melbourne
the following calendar day (e.g. Monday UTC = Tuesday morning Melbourne).

| Run | UTC | Melbourne AEDT (Oct–Apr) | Melbourne AEST (Apr–Oct) |
|---|---|---|---|
| Price check — morning | Mon–Fri 17:00 | Tue–Sat ~4:00 AM | Tue–Sat ~3:00 AM |
| P/E ratio report | Mon–Fri 18:00 | Tue–Sat ~5:00 AM | Tue–Sat ~4:00 AM |
| Price check — afternoon | Mon–Fri 01:00 | Tue–Sat ~12:00 PM | Tue–Sat ~11:00 AM |

Price alerts use **high** priority in Ntfy (will push through Do Not Disturb on most
devices). P/E reports use **default** priority.

---

## Setup Instructions (one-time)

### Step 1 — Get a free Alpha Vantage API key
- Go to [alphavantage.co](https://www.alphavantage.co/support/#api-key) and claim a free key
- The free tier allows 25 requests/day — this tracker uses ~23/day
- Keep the key handy for Step 3

### Step 2 — Install Ntfy on your phone
- Download the **Ntfy** app (iOS or Android) — it's free
- Open the app and subscribe to a topic name that only you know
  (e.g. `johns-etf-alerts-8472` — make it unique so others can't stumble on it)
- Keep note of this topic name — you'll need it in Step 3

### Step 3 — Put this code on GitHub
1. Create a free account at [github.com](https://github.com) if you don't have one
2. Create a new **private** repository (e.g. `BuyOpportunityFinder`)
3. Upload all these files into it (drag and drop works in the GitHub UI)
   - Make sure the folder structure is preserved:
     ```
     BuyOpportunityFinder/
     ├── main.py
     ├── main_pe.py
     ├── config.py
     ├── fetch_prices.py
     ├── fetch_pe.py
     ├── analyse.py
     ├── analyse_pe.py
     ├── notify.py
     ├── requirements.txt
     └── .github/
         └── workflows/
             ├── daily_report.yml
             └── pe_report.yml
     ```

### Step 4 — Add your secrets to GitHub
This keeps your API key and Ntfy topic private and out of your code.

1. In your GitHub repository, click **Settings**
2. In the left sidebar, click **Secrets and variables → Actions**
3. Add the following two secrets:

| Secret name | Value |
|---|---|
| `NTFY_TOPIC` | Your Ntfy topic name (e.g. `johns-etf-alerts-8472`) |
| `ALPHA_VANTAGE_KEY` | Your Alpha Vantage API key |

### Step 5 — Test it manually
1. In your GitHub repo, click the **Actions** tab
2. Click **Daily ETF Report** in the left sidebar
3. Click **Run workflow → Run workflow**
4. Watch the logs — you should see prices being fetched
5. If anything moved 4%+, your phone will buzz

That's it — both workflows will now run automatically every weekday. ✅

---

## Customising your watchlist

Edit the `WATCHLIST` dictionary in `config.py`. Follow the same format:
```python
"TICKER": "Friendly name",
```

Alpha Vantage does not support NZX or ASX tickers on the free tier. Instead, this
tracker follows the underlying US ETFs that your NZX/ASX funds invest in — the
price movements are essentially identical, which is all we need for buy/sell signals.

For example, SmartShares Total World (TWH.NZ) tracks Vanguard Total World (VT),
so we watch `VT` directly.

## Changing the alert threshold

In `config.py`, change this line:
```python
ALERT_THRESHOLD_PCT = 4.0
```
to whatever percentage you prefer.

## Changing the P/E threshold

In `config.py`, change this line:
```python
PE_ALERT_THRESHOLD = 23.0
```
ETFs above this value are flagged as expensive; below as potential buys.

---

## Your current watchlists

### Price watchlist (10 ETFs — checked twice daily)

| Ticker | Fund Name | What it proxies | Exchange |
|---|---|---|---|
| VDE | Vanguard Energy Index | Direct holding | NYSE |
| PHO | Invesco Water Resources | Direct holding | NYSE |
| AAAU | Goldman Sachs Physical Gold | Direct holding | NYSE |
| GLTR | Aberdeen Physical Precious Metals | Direct holding | NYSE |
| VT | Vanguard Total World | SmartShares TWH.NZ | NYSE |
| VWO | Vanguard Emerging Markets | SmartShares EMF.NZ | NYSE |
| VOO | Vanguard S&P 500 | SmartShares USF.NZ | NYSE |
| GLD | SPDR Gold Shares | SmartShares GLD.NZ | NYSE |
| XME | SPDR Metals & Mining | SmartShares AU Resources | NYSE |
| DVY | iShares Dividend Select | SmartShares AU Dividend | NYSE |

### P/E watchlist (9 ETFs — 3 checked per day on rotation)

| Ticker | Fund Name |
|---|---|
| VOO | S&P 500 |
| VT | Vanguard Total World |
| VWO | Vanguard Emerging Markets |
| DVY | iShares Dividend Select |
| VDE | Vanguard Energy Index |
| PHO | Invesco Water Resources |
| XME | SPDR Metals & Mining |
| EFA | iShares MSCI EAFE (developed markets ex-US) |
| QQQ | Invesco Nasdaq-100 |

Note: commodity ETFs (AAAU, GLTR, GLD) are excluded from the P/E watchlist —
physical metal holders have no earnings and therefore no meaningful P/E ratio.

---

## API request budget

Alpha Vantage free tier: **25 requests/day**

| Workflow | Runs/day | ETFs | Requests |
|---|---|---|---|
| Price tracker | 2 | 10 | 20 |
| P/E tracker | 1 | 3 (rotation) | 3 |
| **Total** | | | **23/day** ✅ |
