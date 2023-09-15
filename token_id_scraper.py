import requests
import os
import re
from bs4 import BeautifulSoup
import json
import time

# Read the IPFS hashes from ipfshashes.txt
with open("ipfshashes.txt", "r") as file:
    lines = [line.strip().replace('\0', '') for line in file]

# Read the checked hashes from checked_hashes.txt
checked_hashes = set()
checked_hashes_filepath = "checked_hashes.txt"
if os.path.exists(checked_hashes_filepath):
    with open(checked_hashes_filepath, "r") as file:
        checked_hashes = set(line.strip() for line in file)

ipfs_hashes = []
for line in lines:
    match = re.search(r"\.(\S+)\s*$", line)
    if match:
        ipfs_hash = match.group(1)
        if ipfs_hash not in checked_hashes:
            ipfs_hashes.append(ipfs_hash)
            # Add the hash to checked_hashes and update the checked_hashes.txt
            checked_hashes.add(ipfs_hash)
            with open(checked_hashes_filepath, "a") as file:
                file.write(ipfs_hash + "\n")

if not ipfs_hashes:
    print("No new IPFS hashes found in ipfshashes.txt or all hashes already checked.")
else:
    print(f"Found {len(ipfs_hashes)} new IPFS hashes in ipfshashes.txt.")

# Scrape every 99th JSON file
reddit_links = set()
names_found = set()

for ipfs_hash in ipfs_hashes:
    base_url = f"https://ipfs.io/ipfs/{ipfs_hash}/"
    print(f"Accessing base URL: {base_url}")
    response = requests.get(base_url)
    time.sleep(0.01)  # 1-second delay after page load

    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    # Extract .json file links
    json_links = [link["href"] for link in links if link["href"].endswith(".json")]

    # Extract the token IDs
    token_ids = [int(re.search(r"(\d+)\.json", link).group(1)) for link in json_links if
                 re.search(r"(\d+)\.json", link)]


    # Scrape every 99th JSON file, this variable depends on the token collection sizes. A better implementation would be to begin checking at the last valid token and work back from there, should be updated at some point. 
    for token_id in token_ids[::99]:
        json_url = f"{base_url}{token_id}.json"
        print(f"Scraping JSON URL: {json_url}")
        json_response = requests.get(json_url)
        time.sleep(0.01)  # 1-second delay after page load

        try:
            metadata = json.loads(json_response.text)

            # Check if the name is unique (ignoring the #number part)
            name = re.sub(r' #\d+', '', metadata["name"])
            if name not in names_found:
                names_found.add(name)
                reddit_link = metadata["external_link"]
                reddit_links.add(reddit_link)
                print(f"Unique name found: {metadata['name']}, Reddit link: {reddit_link}")
                # Write the Reddit link to redditlinks.txt as soon as it's found
                with open("redditlinks.txt", "a") as file:
                    file.write(reddit_link + "\n")
        except json.JSONDecodeError:
            print(f"Error decoding JSON at {json_url}")

print("Script finished. Check redditlinks.txt for the results.")
