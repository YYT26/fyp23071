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

# Set the options for Chrome
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode, comment this line if you want to see the browser window
chrome_options.add_argument("--log-level=3")
chrome_options.binary_location = chrome_binary_path

# Create the ChromeDriver service
service = Service(chromedriver_path)

# Create the ChromeDriver instance
driver = webdriver.Chrome(service=service, options=chrome_options)

file = "LIHKG_News_會封.xlsx"

# Load the LIHKG page
df = pd.read_excel(file)
if os.path.isfile(file[:-5]+'_result'+'.xlsx'):
    cur_result = pd.read_excel(file[:-5]+'_result'+'.xlsx')
    done = list(cur_result["link"].values)
    link = list(cur_result["link"].values)
    titles = list(cur_result["title"].values)
    contents = list(cur_result["content"].values)
    allemojis = list(cur_result["emojis"].values)
    times = list(cur_result["time"].values)
else:
    done = []
    link = []
    titles = []
    contents = []
    allemojis = []
    times = []

for index, row in df.iterrows():
    if row['link'] in done:
        continue
    x = 1
    while True:
        count = 0
        b = False
        l = row['link'][:-1]+str(x)
        driver.get(l)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        time.sleep(4)
        first_ele = driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div[2]/div[2]/div[1]")
        if len(first_ele) == 0:
            if len(driver.find_elements(By.XPATH, "/html/body/div[1]/div[2]/div[2]/div/div[2]/div/div[2]/div[1]/div/div[1]")) == 0:
                break

        panel = soup("div",{"id":"rightPanel"})
        if len(panel) == 0:
            break
        
        panel = panel[0]
        comments = panel.find_all("div",recursive=False)[1].find_all("div",recursive=False)
        try:
            comments = comments[len(comments)-1].find_all("div",recursive=False)
        except:
            continue

        for i in range(1,len(comments)):
            div = comments[i]
            try:
                content = div.find('div').find('div').find('div')
                if content == None:
                    continue
            except:
                continue

            emojis = []
            for j in content.findAll('img'):
                try:
                    emojis.append(j['alt'])
                except:
                    a=1
            try:
                times.append(div("span")[3]['data-tip'])
            except:
                times.append('')
            contents.append(content.get_text())
            link.append(l)
            titles.append(row['text'])
            allemojis.append(','.join(emojis))
            i += 1
        x += 1
    
    result_df = pd.DataFrame({"link":link,"title":titles,"time":times,"content":contents,"emojis":allemojis})
    result_df.to_excel(file[:-5]+'_result'+'.xlsx', index=False, engine='xlsxwriter')
    print("done:",index,l,len(contents))
    
#print(result_df)

