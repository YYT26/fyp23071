

# browser = webdriver.Chrome(r"C:\Users\Sin Hoi Yan\Downloads\chromedriver_win32\chromedriver.exe")

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import os
import re

# Set the path to the ChromeDriver executable
chrome_binary_path = r"C:\Users\Sin Hoi Yan\Downloads\chrome-win64 (1)\chrome-win64\chrome.exe"

# Set the path to the Chrome binary
chromedriver_path = r"C:\Users\Sin Hoi Yan\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Update this with the correct path to your Chrome binary

# Set the URL of the Yelp page you want to scrape
url = "https://lihkg.com/category/2"

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

result_df.to_excel('LIHKG_News.xlsx', index=False)
