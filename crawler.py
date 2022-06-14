import time
from selenium import webdriver
import psycopg2
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
# import chromedriver_autoinstaller as chromedriver

# chromedriver.install()

# chrome_options = webdriver.ChromeOptions()
# wd = webdriver.Chrome(options=chrome_options)

# wd.get('https://www.tgju.org/profile/price_dollar_rl/history')

conn = psycopg2.connect(host='localhost', database='data', user='ghazal', password='qwerty')

cur = conn.cursor()
cur.execute('CREATE TABLE prices (id SERIAL PRIMARY KEY, released_date DATE, closed_price INT);')
cur.close()
conn.close()