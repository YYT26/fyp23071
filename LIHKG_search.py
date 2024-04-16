# -*- coding: utf-8 -*-

# browser = webdriver.Chrome(r"C:\Users\Sin Hoi Yan\Downloads\chromedriver_win32\chromedriver.exe")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
import re
import time

# Set the path to the ChromeDriver executable
chrome_binary_path = r"C:\Users\Sin Hoi Yan\Downloads\chrome-win64 (1)\chrome-win64\chrome.exe"

# Set the path to the Chrome binary
chromedriver_path = r"C:\Users\Sin Hoi Yan\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Update this with the correct path to your Chrome binary

# Set the URL of the Yelp page you want to scrape
search_string = "會封"
url = "https://lihkg.com/search?q=" + search_string

# Set the options for Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode, comment this line if you want to see the browser window
chrome_options.binary_location = chrome_binary_path

# Create the ChromeDriver service
service = Service(chromedriver_path)

# Create the ChromeDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

# Load the LIHKG page
driver.get(url)
time.sleep(0.1)
for _ in range(50):
    driver.execute_script("document.getElementById('leftPanel').scrollTo(0, document.getElementById('leftPanel').scrollHeight);")
    time.sleep(0.2)
time.sleep(0.5)
soup = BeautifulSoup(driver.page_source, 'html.parser')

# print(soup.prettify())

# store some variables
result_df = pd.DataFrame(columns=['link', 'text'])

# get all the links in LIHKG hot page
list_of_a_elements = driver.find_elements(By.CSS_SELECTOR, 'a')

for ele in list_of_a_elements:
    ele_href = ele.get_attribute('href')
    if re.search(r'thread/\d+/page', ele_href):
        post_text = ele.find_element(By.XPATH, 'following-sibling::*[1]').get_attribute('innerText')
        index = len(result_df) + 1
        result_df.at[index, 'link'] = ele_href
        result_df.at[index, 'text'] = post_text

# driver.get(f"https://lihkg.com/api_v2/thread/search?q={search_string}&page=1&count=30&sort=score&type=thread")
# print(driver.page_source)
result_df.to_excel('LIHKG_News_'+search_string+'.xlsx', index=False)
print(result_df)

