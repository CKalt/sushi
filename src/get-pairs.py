import requests
import json
import os

def fetch_sushiswap_pairs():
    url = 'https://api.thegraph.com/subgraphs/name/sushiswap/exchange'
    skip = 0  # Number of records to skip
    limit = 10  # Number of records per page
    all_pairs = {}  # To store all fetched pairs

    # Create 'data' directory if it doesn't exist
    if not os.path.exists('data'):
        os.makedirs('data')

    while True:  # Continue fetching until there are no more pairs to fetch
        query = f'''
        {{
          pairs(first: {limit}, skip: {skip}) {{
            id
            token0 {{
              id
              symbol
            }}
            token1 {{
              id
              symbol
            }}
          }}
        }}
        '''
        
        response = requests.post(url, json={'query': query})
        data = json.loads(response.text)
        
        pairs_data = data.get("data", {}).get("pairs", [])
        
        if len(pairs_data) == 0:  # No more pairs to fetch
            break

        for pair in pairs_data:
            token0 = pair.get("token0", {}).get("symbol", "Unknown")
            token1 = pair.get("token1", {}).get("symbol", "Unknown")
            pair_key = f"{token0}/{token1}"

            # Add the fetched pair to the all_pairs dictionary
            all_pairs[pair_key] = pair

        # Print a progress indicator
        print(f"Fetched {skip + len(pairs_data)} pairs so far...")
        
        skip += limit  # Increment skip for the next iteration

    # Save all fetched pairs to 'data/pairs.json'
    with open('data/pairs.json', 'w') as f:
        json.dump(all_pairs, f, indent=4)

    print("Fetching complete. Data saved to 'data/pairs.json'.")

if __name__ == "__main__":
    fetch_sushiswap_pairs()
