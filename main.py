import requests
import json
import random
import os
import csv
from datetime import datetime

def fetch_masked_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15"
    ]
    return {"User-Agent": random.choice(user_agents), "Accept": "application/json"}

def process_node_harvest():
    tokens = "bitcoin,ethereum,solana,ripple,cardano,binancecoin,polkadot,dogecoin,chainlink,avalanche-2"
    # FIXED: Proper URL construction with query parameters
    primary_url = f"https://api.coingecko.com/api/v3/simple/price?ids={tokens}&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true"
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    row_data = None
    
    try:
        # Attempt Primary Data Fetch
        response = requests.get(primary_url, headers=fetch_masked_headers(), timeout=12)
        if response.status_code == 200:
            raw_data = response.json()
            btc = raw_data.get('bitcoin', {})
            eth = raw_data.get('ethereum', {})
            sol = raw_data.get('solana', {})
            
            row_data = [
                timestamp,
                btc.get('usd'), btc.get('usd_24h_vol'), btc.get('usd_24h_change'),
                eth.get('usd'), eth.get('usd_24h_vol'), eth.get('usd_24h_change'),
                sol.get('usd'), sol.get('usd_24h_vol'), sol.get('usd_24h_change')
            ]
            print("PRIMARY_ENGINE_SUCCESS: Data parsed.")
        else:
            raise Exception(f"Primary error status code: {response.status_code}")
            
    except Exception as network_error:
        print(f"PRIMARY_FAILED: {str(network_error)}. Swapping to fail-safe...")
        # FIXED: Proper Binance API endpoint with query parameters
        try:
            backup_url = "https://api.binance.com/api/v3/ticker/price?symbols=[%22BTCUSDT%22,%22ETHUSDT%22,%22SOLUSDT%22]"
            backup_response = requests.get(backup_url, headers=fetch_masked_headers(), timeout=10)
            if backup_response.status_code == 200:
                prices = {item['symbol']: float(item['price']) for item in backup_response.json() if item['symbol'] in ['BTCUSDT', 'ETHUSDT', 'SOLUSDT']}
                
                row_data = [
                    timestamp,
                    prices.get('BTCUSDT'), 0.0, 0.0,
                    prices.get('ETHUSDT'), 0.0, 0.0,
                    prices.get('SOLUSDT'), 0.0, 0.0
                ]
                print("FAIL_SAFE_ENGINE_SUCCESS: Backup data parsed.")
        except Exception as critical_fault:
            print(f"CRITICAL_OFFLINE_FAIL: {str(critical_fault)}")

    # Write data row to file if successfully collected from either source
    if row_data:
        file_name = "crypto_data_feed.csv"
        file_exists = os.path.isfile(file_name)
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    "Timestamp", 
                    "BTC_Price", "BTC_Vol_24h", "BTC_Change_24h",
                    "ETH_Price", "ETH_Vol_24h", "ETH_Change_24h",
                    "SOL_Price", "SOL_Vol_24h", "SOL_Change_24h"
                ])
            writer.writerow(row_data)
        print("SUCCESS: Data file updated securely.")

if __name__ == "__main__":
    process_node_harvest()
