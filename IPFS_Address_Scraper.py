import requests
import json
import time
import os
import re

# Read the addresses from the addresses.txt file
with open("contract_proxy_routes.txt", "r") as file:
    urls = [line.strip() for line in file]

# Extract addresses from the URLs
address_pattern = re.compile(r'https://polygonscan\.com/address/([^#]+)#readProxyContract')
addresses = [address_pattern.search(url).group(1) for url in urls]

# Define the headers to use in the request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Referer': 'https://polygonscan.com/',
    'Origin': 'https://polygonscan.com',
    'Content-Type': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,en-GB;q=0.8,nl;q=0.7',
    'DNT': '1',
}

# Iterate through the addresses and input values
with open("ipfshashes.txt", "w") as output_file:
    for address in addresses:
        hash_found = False
        for input_value in range(10):
            if hash_found:
                break

            print(f"Processing Address: {address}, Input value: {input_value}")

            # Define the payload to use in the request
            payload = {
                "jsonrpc": "2.0",
                "id": 1,
                "method": "eth_call",
                "params": [
                    {
                        "from": "0x0000000000000000000000000000000000000000",
                        "data": f"0x726f16d8000000000000000000000000000000000000000000000000000000000000000{input_value}",
                        "to": address
                    },
                    "latest"
                ]
            }

            # Send the request to the server and parse the response
            response = requests.post('https://polygon-rpc.com/', headers=headers, data=json.dumps(payload))
            response_data = json.loads(response.text)

            # Extract the result from the response data and parse it as a string
            result = response_data.get('result')
            if result and all(c in '0123456789abcdefABCDEF' for c in result[2:]):
                result_string = bytes.fromhex(result[2:].replace("00", "").replace(" ", "").replace(".", "")).decode(
                    'utf-8', errors='ignore')

                # Write the result string to the output file
                output_file.write(f"Address: {address}, Input value: {input_value}, Hash: {result_string}\n")
                print(f"Hash: {result_string}")
            else:
                output_file.write(f"Address: {address}, Input value: {input_value}, No valid response.\n")
                print("No valid response.")
                break

            # Avoid spamming calls
            time.sleep(0.2)
