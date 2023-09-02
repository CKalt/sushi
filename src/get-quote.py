import requests
import json
import sys
import os

def fetch_sushiswap_price(pair_id):
    # Endpoint for the Sushiswap Subgraph API
    url = 'https://api.thegraph.com/subgraphs/name/sushiswap/exchange'

    # Query for the pair
    query = f'''
    {{
      pairs(where: {{id: "{pair_id}"}}) {{
        id
        token0 {{
          id
          symbol
        }}
        token1 {{
          id
          symbol
        }}
        reserve0
        reserve1
      }}
    }}
    '''
    # Perform the API call
    response = requests.post(url, json={'query': query})
    
    # Parse the response
    data = json.loads(response.text)
    
    # Extract relevant information
    pairs_data = data.get("data", {}).get("pairs", [{}])[0]

    token0 = pairs_data.get("token0", {}).get("symbol", "Unknown")
    token1 = pairs_data.get("token1", {}).get("symbol", "Unknown")
    reserve0 = float(pairs_data.get("reserve0", 0))
    reserve1 = float(pairs_data.get("reserve1", 0))

    # Check token positions and adjust calculation accordingly
    base_token, quote_token = pair_key.split('/')

    if base_token == token0:
        if reserve1 == 0:
            print("No liquidity available for the pair.")
            return
        price = 1 / (reserve0 / reserve1)
    elif base_token == token1:
        if reserve0 == 0:
            print("No liquidity available for the pair.")
            return
        price = 1 / (reserve1 / reserve0)
    else:
        print("Base token not found in pair data.")
        return

    print(f"The current price of {base_token}/{quote_token} is approximately {price}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a pair key like ETH/USDT.")
        sys.exit(1)
    
    pair_key = sys.argv[1]

    # Check if data/pairs.json exists
    if not os.path.exists('data/pairs.json'):
        print("data/pairs.json file does not exist.")
        sys.exit(1)

    # Load pairs from data/pairs.json
    with open('data/pairs.json', 'r') as f:
        pairs_data = json.load(f)
    
    # Look up pair ID using the given key
    pair_data = pairs_data.get(pair_key)
    
    if pair_data:
        pair_id = pair_data.get("id")
        if pair_id:
            fetch_sushiswap_price(pair_id)
        else:
            print(f"Could not find an ID for the pair {pair_key}.")
    else:
        print(f"Could not find the pair {pair_key} in data/pairs.json.")
