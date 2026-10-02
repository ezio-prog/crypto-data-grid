import requests
import json
import random
import os
import csv
from datetime import datetime

def fetch_masked_headers():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"
    ]
    return {"User-Agent": random.choice(user_agents), "Accept": "application/json"}

def process_node_harvest():
    tokens = "bitcoin,ethereum,solana,ripple,cardano,binancecoin,polkadot,dogecoin,chainlink,avalanche-2"
    
    # FIXED FULL PATH URL: Explicitly maps the structural API endpoints cleanly
    url = f"https://coingecko.com{tokens}&order=market_cap_desc&per_page=10&page=1&sparkline=false&price_change_percentage=24h"
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    compiled_row = [timestamp]
    headers_list = ["Timestamp"]
    
    try:
        response = requests.get(url, headers=fetch_masked_headers(), timeout=15)
        if response.status_code == 200:
            market_data = response.json()
            
            # Loop through each token payload to harvest dense metrics arrays
            for coin in market_data:
                symbol = coin.get('symbol', '').upper()
                
                compiled_row.extend([
                    coin.get('current_price'),
                    coin.get('market_cap'),
                    coin.get('total_volume'),
                    coin.get('high_24h'),
                    coin.get('low_24h'),
                    coin.get('price_change_percentage_24h'),
                    coin.get('circulating_supply')
                ])
                
                headers_list.extend([
                    f"{symbol}_Price", f"{symbol}_MarketCap", f"{symbol}_Vol24h",
                    f"{symbol}_High24h", f"{symbol}_Low24h", f"{symbol}_Change24h", f"{symbol}_Supply"
                ])
                
            file_name = "crypto_data_feed.csv"
            file_exists = os.path.isfile(file_name)
            
            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(headers_list)
                writer.writerow(compiled_row)
            print(f"SUCCESS: Dense data array compiled for {len(market_data)} assets.")
        else:
            print(f"GATEWAY_REJECTION: Status code {response.status_code}")
    except Exception as e:
        print(f"HARVEST_CRITICAL_FAIL: {str(e)}")

if __name__ == "__main__":
    process_node_harvest()
