import socket
import time
import json
import requests
import os

print("[producer] ✅ Script is starting...", flush=True)

# Configuration
HOST = "0.0.0.0"  # Listen on all interfaces
PORT = 9998       # Port to stream on
TICKERS = ["AAPL", "MSFT", "GOOG"]
API_KEY = os.getenv("API_KEY")  # Read from environment variable

def get_prices():
    symbols = ",".join(TICKERS)
    url = f"https://financialmodelingprep.com/api/v3/quote-short/{symbols}?apikey={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"API error: {response.status_code} {response.text}")
            return []
    except Exception as e:
        print(f"Error fetching stock prices: {e}")
        return []

# Start socket server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print(f"[producer] Waiting for Spark to connect on {HOST}:{PORT}...")
    
    conn, addr = server_socket.accept()
    print(f"[producer] Connection established with Spark at {addr}")

    with conn:
        while True:
            prices = get_prices()
            for price in prices:
                record = {
                    "symbol": price["symbol"],
                    "price": price["price"],
                    "timestamp": int(time.time())
                }
                message = json.dumps(record) + "\n"
                conn.sendall(message.encode("utf-8"))
                print(f"[producer] Sent: {message.strip()}")
            time.sleep(10)
