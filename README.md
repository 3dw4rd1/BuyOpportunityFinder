# 📈 ETF Tracker — Daily Buy Opportunity Notifier

Automatically checks your ETF watchlist every morning and sends a push
notification to your phone (via Ntfy) if anything moves 3% or more.

Runs entirely for free on GitHub Actions — no server needed.

---

## How it works

1. Every weekday at 6:00 AM NZT, GitHub runs the script automatically
2. It fetches the latest closing prices for all 10 ETFs via Yahoo Finance
3. It compares each price to the previous day's close
4. If anything moved ≥ 3%, you get a push notification on your phone
5. On quiet days, nothing is sent

---

## Setup Instructions (one-time)

### Step 1 — Install Ntfy on your phone
- Download the **Ntfy** app (iOS or Android) — it's free
- Open the app and subscribe to a topic name that only you know
  (e.g. `johns-etf-alerts-8472` — make it unique so others can't stumble on it)
- Keep note of this topic name — you'll need it in Step 3

### Step 2 — Put this code on GitHub
1. Create a free account at [github.com](https://github.com) if you don't have one
2. Create a new **private** repository (e.g. `etf-tracker`)
3. Upload all these files into it (drag and drop works in the GitHub UI)
   - Make sure the folder structure is preserved:
     ```
     etf-tracker/
     ├── main.py
     ├── config.py
     ├── fetch_prices.py
     ├── analyse.py
     ├── notify.py
     ├── requirements.txt
     └── .github/
         └── workflows/
             └── daily_report.yml
     ```

### Step 3 — Add your Ntfy topic as a GitHub Secret
This keeps your topic name private and out of your code.

1. In your GitHub repository, click **Settings**
2. In the left sidebar, click **Secrets and variables → Actions**
3. Click **New repository secret**
4. Name: `NTFY_TOPIC`
5. Value: your topic name (e.g. `johns-etf-alerts-8472`)
6. Click **Add secret**

### Step 4 — Test it manually
1. In your GitHub repo, click the **Actions** tab
2. Click **Daily ETF Report** in the left sidebar
3. Click **Run workflow → Run workflow**
4. Watch the logs — you should see prices being fetched
5. If anything moved 3%+, your phone will buzz!

That's it — it'll now run automatically every weekday morning. ✅

---

## Customising your watchlist

Edit `config.py` to add or remove ETFs. Just follow the same format:
```python
"TICKER": "Friendly name",
```

For NZX-listed funds, add `.NZ` to the ticker (e.g. `"USF.NZ"`).
For US/ASX-listed funds, use the ticker as-is (e.g. `"VDE"`).

## Changing the alert threshold

In `config.py`, change this line:
```python
ALERT_THRESHOLD_PCT = 3.0
```
to whatever percentage you prefer.

---

## Your current watchlist

| Ticker   | Fund Name                              | Exchange |
|----------|----------------------------------------|----------|
| VDE      | Vanguard Energy Index                  | NYSE     |
| PHO      | Invesco Water Resources                | NYSE     |
| AAAU     | Goldman Sachs Physical Gold            | NYSE     |
| GLTR     | Aberdeen Physical Precious Metals      | NYSE     |
| TWH.NZ   | SmartShares Total World (NZD Hedged)   | NZX      |
| EMF.NZ   | SmartShares Emerging Markets           | NZX      |
| ASR.NZ   | SmartShares Australian Resources       | NZX      |
| ASD.NZ   | SmartShares Australian Dividend        | NZX      |
| USF.NZ   | SmartShares US500                      | NZX      |
| GLD.NZ   | SmartShares Gold ETF                   | NZX      |
