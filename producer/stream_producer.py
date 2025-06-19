import os
import time
import json
import requests
from datetime import datetime

print("[producer] ✅ Script is starting...")

TICKERS = ["AAPL", "MSFT", "GOOG"]
API_KEY = os.getenv("API_KEY")
OUT_DIR = "/app/shared_volume/stream_data"
os.makedirs(OUT_DIR, exist_ok=True)

def get_prices():
    symbols = ",".join(TICKERS)
    url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbols}?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[producer] API error: {response.status_code} {response.text}")
            return []
    except Exception as e:
        print(f"[producer] ❌ Error fetching stock prices: {e}")
        return []

while True:
    prices = get_prices()
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    filepath = os.path.join(OUT_DIR, f"tickers_{timestamp}.json")

    try:
        with open(filepath, "w") as f:
            for price in prices:
                record = {
                    "symbol": price["symbol"],
                    "price": price["price"],
                    "timestamp": int(time.time())
                }
                f.write(json.dumps(record) + "\n")
            print(f"[producer] ✅ Wrote {len(prices)} records to {filepath}")
    except Exception as e:
        print(f"[producer] ❌ Failed to write file: {e}")

    time.sleep(10)
