import requests
import json
import random
from datetime import datetime

def fetch_masked_headers():
    # Rotates browser footprints so cloud servers look like ordinary everyday laptop users
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    ]
    return {
        "User-Agent": random.choice(user_agents),
        "Accept": "application/json"
    }

def process_node_harvest():
    # Targets the top 10 highest value market cap tokens for heavy data mass
    tokens = "bitcoin,ethereum,solana,ripple,cardano,binancecoin,polkadot,dogecoin,chainlink,avalanche-2"
    primary_url = f"https://coingecko.com{tokens}&vs_currencies=usd&include_24hr_vol=true&include_24hr_change=true"
    
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    try:
        # Attempt to harvest from primary stream engine
        response = requests.get(primary_url, headers=fetch_masked_headers(), timeout=12)
        if response.status_code == 200:
            raw_data = response.json()
            
            # Formats unified global layout framework for Web3 buyers
            payload = {
                "status": "NODE_SECURE_OK",
                "engine_source": "PRIMARY_GECKO",
                "timestamp": timestamp,
                "dataset": {
                    token: {
                        "price_usd": metrics.get("usd"),
                        "vol_24h": metrics.get("usd_24h_vol"),
                        "change_24h": metrics.get("usd_24h_change")
                    } for token, metrics in raw_data.items()
                }
            }
            print(f"GRID_TELEMETRY_STREAM: {json.dumps(payload)}")
            return payload
        else:
            raise Exception(f"Primary filter encountered status code: {response.status_code}")
            
    except Exception as network_error:
        # EMERGENCY DECENTRALIZED FALLBACK ENGINE
        # If the primary provider blocks or throttles the connection, instantly fall back to Binance API endpoints
        try:
            backup_url = "https://binance.com[%22BTCUSDT%22,%22ETHUSDT%22,%22SOLUSDT%22]"
            backup_response = requests.get(backup_url, headers=fetch_masked_headers(), timeout=10)
            
            payload = {
                "status": "FAIL_SAFE_SHIELD_ACTIVE",
                "engine_source": "BACKUP_BINANCE",
                "timestamp": timestamp,
                "incident_log": str(network_error),
                "dataset": backup_response.json()
            }
            print(f"GRID_TELEMETRY_STREAM: {json.dumps(payload)}")
            return payload
        except Exception as critical_fault:
            print(f"CRITICAL_OFFLINE_FAIL: {str(critical_fault)}")

if __name__ == "__main__":
    process_node_harvest()
