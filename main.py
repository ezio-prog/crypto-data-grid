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
    # Direct endpoint for top trending assets globally
    trending_url = "https://api.coingecko.com/api/v3/search/trending"
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    row_data = [timestamp]
    
    try:
        response = requests.get(trending_url, headers=fetch_masked_headers(), timeout=12)
        if response.status_code == 200:
            trending_coins = response.json().get('coins', [])
            
            # Select and parse the top 3 trending assets dynamically
            top_3 = trending_coins[:3]
            
            for index, coin in enumerate(top_3):
                item = coin.get('item', {})
                name = item.get('name', 'Unknown')
                symbol = item.get('symbol', 'UNK').upper()
                rank = item.get('market_cap_rank', 'N/A')
                
                # Fetch clean structural metrics safely
                data = item.get('data', {})
                price = data.get('price', 0.0)
                
                # If price is inside an HTML tag string fallback, clean it up
                if isinstance(price, str):
                    price = price.split('$')[-1].replace(',', '').strip()
                
                row_data.extend([name, symbol, rank, price])
                
            file_name = "crypto_data_feed.csv"
            file_exists = os.path.isfile(file_name)
            
            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    # Initialize clean schema for the top 3 trending metrics positions
                    writer.writerow([
                        "Timestamp",
                        "Trend1_Name", "Trend1_Symbol", "Trend1_Rank", "Trend1_Price",
                        "Trend2_Name", "Trend2_Symbol", "Trend2_Rank", "Trend2_Price",
                        "Trend3_Name", "Trend3_Symbol", "Trend3_Rank", "Trend3_Price"
                    ])
                writer.writerow(row_data)
            print("SUCCESS: Dynamic top trending data points appended safely.")
        else:
            print(f"GATEWAY_REJECTION: Status code {response.status_code}")
            
    except Exception as network_error:
        print(f"HARVEST_CRITICAL_FAIL: {str(network_error)}")

if __name__ == "__main__":
    process_node_harvest()
