import os
import requests
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Specify the path for Chromedriver
webdriver_service = Service('[Path to chromedriver.exe')

# Initialize a WebDriver
driver = webdriver.Chrome(service=webdriver_service)

reddit_main_url = 'https://old.reddit.com'
driver.get(reddit_main_url)

username_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'user')))
password_element = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'passwd')))
login_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#login_login-main .btn')))

username_element.send_keys('Usernamee')
password_element.send_keys('Password')
login_button.click()

# Let's wait for a while to be sure we are logged in
time.sleep(3)

with open("redditlinks.txt", "r") as f:
    reddit_urls = f.read().splitlines()

# Remove duplicate URLs
reddit_urls = list(set(reddit_urls))

folder_name = "Contract_data"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)

if not os.path.exists('checked_addresses'):
    with open('checked_addresses', 'w'): pass

with open("checked_addresses", "r") as f:
    already_checked_urls = f.read().splitlines()

for url in reddit_urls:
    if url in already_checked_urls:
        print(f'{url} was already processed. Skipping...')
        continue
    print(f"Processing {url}...")

    driver.get(url)
    time.sleep(8)

    image_div = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._frontBackground_pqaq2_70')))

    item_name_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'h3._cardName_7kbcu_73')))

    artist_name = 'Unknown'

    artist_name_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div._cardAuthor_7kbcu_79')))

    if artist_name_element.text != 'by Reddit':
        artist_name_element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span._artistName_7kbcu_135')))
        artist_name = artist_name_element.text.split('by ')[-1]
        artist_name = re.sub(r'[\\/*?:"<>|]', '_', artist_name)

    item_name = item_name_element.text.split('#')[0]
    item_name = re.sub(r'[\\/*?:"<>|]', '_', item_name)

    style = image_div.get_attribute('style')

    url_match = re.search(r'url\("(.*?)"\)', style)
    if url_match:
        image_url = url_match.group(1)
    else:
        print('No image URL found')

    img_name = artist_name + '-' + item_name + ".png"
    if os.path.isfile(os.path.join(folder_name, img_name)):
        i = 1
        img_name_without_ext, ext = os.path.splitext(img_name)
        while os.path.isfile(os.path.join(folder_name, img_name)):
            img_name = "{}_{}{}".format(img_name_without_ext, i, ext)
            i += 1

    img_response = requests.get(image_url)
    with open(os.path.join(folder_name, img_name), "wb") as img_file:
        img_file.write(img_response.content)

    with open("gen4_checked.txt", "a") as f:
        f.write(url + "\n")

    time.sleep(1)