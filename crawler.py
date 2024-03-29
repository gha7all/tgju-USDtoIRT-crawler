from config import *
import time
from selenium import webdriver
import psycopg2
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller as chromedriver
from selenium.webdriver.support import expected_conditions as EC

chromedriver.install()
chrome_options = webdriver.ChromeOptions()
wd = webdriver.Chrome(options=chrome_options)
wd.get('https://www.tgju.org/profile/price_dollar_rl/history')
wd.maximize_window()
wd.implicitly_wait(20)

conn = psycopg2.connect(host=host, database=database,
                        user=user, password=password)
cur = conn.cursor()


def create_table():
    cur.execute("""
                CREATE TABLE USDPRICES (id SERIAL PRIMARY KEY, 
                released_date VARCHAR, open_price INT, low_price INT, high_price INT, close_price INT);
                 """
                )
    conn.commit()


def insert_to_db(open_price, low_price, high_price, close_price, date):
    cur.execute("""
                INSERT INTO USDPRICES (released_date, open_price, low_price, high_price, close_price) 
                VALUES(%s, %s, %s, %s, %s);
                """,
                (date, open_price, low_price, high_price, close_price))
    conn.commit()


def calender_setup():
    """
    gets the last entered date and then sets the calender up to 
    the a year before. after the page gets loaded it just finds
    the last page number so we could use it later.
    """
    last_entered = wd.find_element(
        By.XPATH, '//*[@id="table-list"]/tr[1]/td[8]').text
    starting_date = last_entered.replace('1401', '1400')

    calender = wd.find_elements(
        By.XPATH, '//*[@id="main"]/div[1]/div[2]/div[2]/div[1]/div/div[2]')
    for c in calender:
        wd.find_element(
            By.ID, 'history-from').send_keys(starting_date)
        wd.find_element(By.ID, 'history-to').send_keys(last_entered)

    last_page_number = wd.find_element(
        By.XPATH, '/html/body/main/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/div/div[1]/span/a[6]').text

    return int(last_page_number)


def click_next():
    """
    scrolls to the pagination section and clicks on the next buttonm
    """
    element = wd.find_element(By.XPATH,
                              "/html/body/main/div[1]/div[2]/div/div[1]/div/div[3]/div/table/tbody/tr[25]/td[1]")
    wd.execute_script('arguments[0].scrollIntoView(true);', element)
    button = wd.find_element(By.XPATH, '//*[@id="DataTables_Table_0_next"]')
    time.sleep(1)
    ActionChains(wd).move_to_element(button).click().perform()
    time.sleep(2)


def crawler():
    """
    loads every single page and scrapes the prices from the page,
    then by calling the insert_to_db it inserts each record to the database.
    note: due to leap years and having trouble converting them to datetime 
    format it gets gregorian dates from the table.
    """
    create_table()
    last_page_number = calender_setup()
    click_next()
    for page in range(last_page_number):
        number_of_rows = len(wd.find_elements(
            By.XPATH, '//*[@id="table-list"]/tr'))
        time.sleep(1)

        for i in range(1, number_of_rows+1):
            table = wd.find_elements(
                By.XPATH, f'//*[@id="table-list"]/tr[{i}]')
            for t in table:
                open_price = wd.find_element(
                    By.XPATH, f'//*[@id="table-list"]/tr[{i}]/td[1]').text
                open_price = int(open_price.replace(',', ''))

                low_price = wd.find_element(
                    By.XPATH, f'//*[@id="table-list"]/tr[{i}]/td[2]').text
                low_price = int(low_price.replace(',', ''))

                high_price = wd.find_element(
                    By.XPATH, f'//*[@id="table-list"]/tr[{i}]/td[3]').text
                high_price = int(high_price.replace(',', ''))

                close_price = wd.find_element(
                    By.XPATH, f'//*[@id="table-list"]/tr[{i}]/td[4]').text
                close_price = int(close_price.replace(',', ''))

                date = wd.find_element(
                    By.XPATH, f'//*[@id="table-list"]/tr[{i}]/td[7]').text
            if low_price == 0 and high_price == 0 and close_price == 0 and open_price == 0:
                pass
            else:
                print(date, low_price, high_price, open_price, close_price)
                insert_to_db(open_price=open_price, low_price=low_price,
                             high_price=high_price, close_price=close_price, date=date)

        if page == (last_page_number-1):
            pass
        else:
            click_next()


crawler()

wd.quit()
cur.close()
conn.close()
