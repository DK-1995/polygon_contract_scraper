# Polygon Reddit NFT Scraper

This is a personal project to scrape metadata for Reddit's NFT avatar collections. The goal is to collect and organize the metadata and associated media.
Reddit utilizes Polygon blockchain NFTs as the backend for their user avatar system. New avatar collections are released in batches, with the smart contracts and metadata prepared in advance before the actual artworks go live on Reddit.
Thus, this project collects metadata and associated media by scraping various sources:

Polygonscan - for upcoming smart contract addresses
Proxy contracts - to extract IPFS hashes pointing to metadata
IPFS networks - to retrieve JSON metadata files
Reddit - to download the avatar images associated with the tokens

By stitching together data from these sources, the scripts build a complete dataset of the tokens (avatars). This is useful as Reddit distributes avatars across hundreds of contracts, making it difficult to view the collections holistically before they are released. 

This project relies on a number of key packages:
- BeautifulSoup - for parsing and extracting data from HTML 
- Selenium - for automating a Chrome browser to access dynamic content
- re - for regular expressions to parse identifiers
- Requests - for sending HTTP requests to APIs and websites

The scripts scrape data from the Polygon blockchain, IPFS networks, and Reddit itself. They are designed to run sequentially, with each step providing input for the next.

1. `contract_address_parser.py` - Parses a raw copy of Polygonscan contract addresses to extract only the proxy contract addresses. This provides the starting point for scraping.

2. `IPFS_Address_Scraper.py` - Calls the proxy contracts to extract the IPFS hashes associated with each NFT token.

3. `token_id_scraper.py` - Iterates through the IPFS directories to identify valid token IDs and scrape select metadata files. This looks for unique token names and extracts their Reddit links. 

4. `reddit_metadata_scraper.py` - Uses Selenium with headless Chrome to scrape Reddit for the full metadata and images associated with each valid token name.

The goal is primarily to make the data more accessible and organized for people (reddit users) who enjoy collecting and discussing these NFTs. 
