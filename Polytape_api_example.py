import os
import requests
import json
import time

from dotenv import load_dotenv

load_dotenv()
# ==========================================
# CONFIGURATION
# ==========================================
API_URL = "https://api.polytape.xyz"  # Local Testing Endpoint

# sample .env file should contain POLYTAPE_API_KEY=your_api_key_here
API_KEY = os.getenv("POLYTAPE_API_KEY", "your_api_key_here")

# Target Asset Metadata (Gavin Newsom 2028 Democratic Nominee - Yes)
TARGET_ASSET = {
    "question": "Will Gavin Newsom win the 2028 Democratic presidential nomination?",
    "outcome_type": "Yes",
    "asset_id": "54533043819946592547517511176940999955633860128497669742211153063842200957669",
    "condition_id": "0x0f49db97f71c68b1e42a6d16e3de93d85dbf7d4148e3f018eb79e88554be9f75"
}

# ==========================================
# UTILITIES
# ==========================================

def save_json_sample(filename, data):
    """Saves the JSON response to the local 'data_samples' directory."""
    if not os.path.exists("data_samples"):
        os.makedirs("data_samples")
    
    filepath = os.path.join("data_samples", filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"📁 Sample saved to: {filepath}")

def print_pretty_json(title, data):
    """Prints a truncated version of the JSON for terminal readability."""
    print(f"\n--- {title} ---")
    clean_data = json.loads(json.dumps(data))
    
    # Truncate large orderbooks so they don't flood the terminal
    if "bids" in clean_data and isinstance(clean_data["bids"], list):
        clean_data["bids"] = clean_data["bids"][:5] 
    if "asks" in clean_data and isinstance(clean_data["asks"], list):
        clean_data["asks"] = clean_data["asks"][:5] 
        
    print(json.dumps(clean_data, indent=4))

# ==========================================
# POLYTAPE API CLIENT
# ==========================================

class PolyTapeAPI:
    def __init__(self, api_url, api_key):
        self.url = api_url
        self.headers = {
            "x-api-key": api_key, 
            "Content-Type": "application/json"
        }

    def get_orderbook(self, asset_id):
        """Fetches the latest L2 orderbook snapshot for a specific asset."""
        endpoint = f"{self.url}/v1/markets/{asset_id}/orderbook"
        r = requests.get(endpoint, headers=self.headers)
        r.raise_for_status()
        return r.json()

    def simulate_buy(self, asset_id, timestamp, amount_usd):
        """Calculates price impact for a market buy of a specific USD amount."""
        endpoint = f"{self.url}/v1/markets/{asset_id}/simulate/buy"
        payload = {"timestamp": timestamp, "amount_usd": amount_usd}
        r = requests.post(endpoint, headers=self.headers, json=payload)
        return r.json()

    def simulate_sell(self, asset_id, timestamp, amount_sell):
        """Calculates price impact for a market sell of a specific share amount."""
        endpoint = f"{self.url}/v1/markets/{asset_id}/simulate/sell"
        payload = {"timestamp": timestamp, "amount_sell": amount_sell}
        r = requests.post(endpoint, headers=self.headers, json=payload)
        return r.json()

# ==========================================
# MAIN EXECUTION
# ==========================================

def main():
    api = PolyTapeAPI(API_URL, API_KEY)
    asset_id = TARGET_ASSET["asset_id"]
    
    print(f"🚀 Initializing PolyTape API Test")
    print(f"Target: {TARGET_ASSET['question']} ({TARGET_ASSET['outcome_type']})")

    # 1. Fetch and Save Orderbook
    try:
        orderbook = api.get_orderbook(asset_id)
        valid_ts = orderbook['meta']['found_ts']
        
        save_json_sample(f"orderbook_{asset_id[:8]}.json", orderbook)
        print_pretty_json("Live Orderbook Snapshot (Top 5)", orderbook)
        print(f"✅ Found valid historical timestamp: {valid_ts}")
    except Exception as e:
        print(f"❌ Connection Error: Ensure your API is running at {API_URL}")
        print(f"Details: {e}")
        return

    # 2. Simulate Buy ($100,000 USD)
    try:
        print(f"\n1️⃣  Testing /simulate/buy ...")
        buy_res = api.simulate_buy(asset_id, valid_ts, 100000.0)
        save_json_sample(f"buy_sim_{valid_ts}.json", buy_res)
        print_pretty_json("Simulate BUY Result", buy_res)
    except Exception as e:
        print(f"❌ BUY Simulation Failed: {e}")

    # 3. Simulate Sell (100,000 Shares)
    try:
        print(f"\n2️⃣  Testing /simulate/sell ...")
        sell_res = api.simulate_sell(asset_id, valid_ts, 100000.0)
        save_json_sample(f"sell_sim_{valid_ts}.json", sell_res)
        print_pretty_json("Simulate SELL Result", sell_res)
    except Exception as e:
        print(f"❌ SELL Simulation Failed: {e}")

if __name__ == "__main__":
    main()