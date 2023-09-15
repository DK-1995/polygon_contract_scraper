from bs4 import BeautifulSoup

# Load the data from the file with UTF-8 encoding
with open('contract_addresses.txt', 'r', encoding='utf-8') as fp:
    data = fp.read()

# Create a BeautifulSoup object
soup = BeautifulSoup(data, 'html.parser')

# Extract the contract addresses
addresses = [tag.get('href').split('/')[-1].split('#')[0] for tag in soup('a', {'class': 'address-tag'})]

# Format the addresses into URLs
urls = ['https://polygonscan.com/address/' + address + '#readProxyContract' for address in addresses]

# Write the URLs to a .txt file
with open("contract_proxy_routes.txt", "w") as file:
    for url in urls:
        file.write(url + "\n")