from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import csv
import random
x=0
web_timer=20
# Read proxy IPs and ports from the "proxy.txt" file
proxy_list = []
with open("valid_proxy.txt", 'r') as file:
    for line in file:
        proxy_list.append(line.strip())

data = {'Company Name': [], 'First Name': [], 'Last Name': []}

chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument("--headless")

webdriver_service = Service("/usr/local/bin/chromedriver")  # Your chromedriver path
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

with open("tests.csv", 'r') as file:
    csvreaders = csv.reader(file, delimiter=':')
    data1 = list(csvreaders)

with open("tests.csv", 'r') as file:
    csvreader = csv.reader(file, delimiter=':')

    for row in csvreader:
        url = 'https://opencorporates.com/'
        driver.get(url)
        driver.maximize_window()
        time.sleep(web_timer)
        
        # Rotate proxy randomly from the list
        random_proxy = random.choice(proxy_list)
        proxy_ip, proxy_port = random_proxy.split(":")
        chrome_options.add_argument(f'--proxy-server=http://{proxy_ip}:{proxy_port}')
        print(random_proxy)
        # Rest of your code remains the same...
        # (replace the rest of your code here)
        driver.find_element(By.XPATH,'//input[@name="q"]').send_keys(row[0])
        time.sleep(2)
        driver.find_element(By.XPATH,'//button[@class="oc-home-search_button"]').click()
        time.sleep(2)
        
        try:
            try:
                driver.find_element(By.XPATH,'//a[@class ="company_search_result current_active"]').click()
                time.sleep(2)
            
            except:
                driver.find_element(By.XPATH,'//a[@class ="company_search_result in_existence"]').click()
                time.sleep(2)
        except:
            x=x+1
            driver.find_element(By.XPATH,'//input[@placeholder="Company name or number"]').send_keys(data1[x][0])
            time.sleep(2)
            driver.find_element(By.XPATH,'//button[@class="oc-header-search__button"]').click()
            time.sleep(2)
            try:
                driver.find_element(By.XPATH,'//a[@class ="company_search_result current_active"]').click()
                time.sleep(2)
            except:
                driver.find_element(By.XPATH,'//a[@class ="company_search_result in_existence"]').click()
                time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'lxml')
        infos = soup.find(class_="agent_name")
        name = infos.string.split(',')
        data['Company Name'].append(row[0])
        try:
            last_name = name[0]
            first_name = name[1]
            data['First Name'].append(first_name)
            data['Last Name'].append(last_name)
        except:
            full= infos.string
            data['First Name'].append(full)
        x=x+1
        web_timer=3
df = pd.DataFrame.from_dict(data)
df.to_csv('Names.csv', index=False)

driver.quit()