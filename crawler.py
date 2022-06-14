import time
from selenium import webdriver
import psycopg2
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller as chromedriver


def calender_setup():
    last_entered = wd.find_element(
        By.XPATH, '//*[@id="table-list"]/tr[1]/td[8]').text
    starting_date = last_entered.replace('1401', '1400')

    calender = wd.find_elements(
        By.XPATH, '//*[@id="main"]/div[1]/div[2]/div[2]/div[1]/div/div[2]')
    for c in calender:
        from_date = wd.find_element(
            By.ID, 'history-from').send_keys(starting_date)
        to_date = wd.find_element(By.ID, 'history-to').send_keys(last_entered)
  
    last_page_number = wd.find_element(
        By.XPATH, '/html/body/main/div[1]/div[2]/div[2]/div[1]/div/div[3]/div/div[2]/div/div[1]/span/a[6]').text

    return last_page_number


def click_next():
    element = wd.find_element(By.XPATH,
                              "/html/body/main/div[1]/div[2]/div/div[1]/div/div[3]/div/table/tbody/tr[25]/td[1]")
    wd.execute_script('arguments[0].scrollIntoView(true);', element)
    button = wd.find_element(By.XPATH, '//*[@id="DataTables_Table_0_next"]')
    ActionChains(wd).move_to_element(button).click().perform()
    time.sleep(3)


def crawler():
    last_page_number = calender_setup()

    for page in range(int(last_page_number)+1):
        # since the website ignores the first click, we don't miss the first page by clicking on the next page here
        if page == int(last_page_number):
            break
            
        else:
            click_next()
            
        for i in range(1, 31):
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
                    By.XPATH, f'//*[@id="table-list"]/tr[{i}]/td[8]').text

            print(open_price, low_price, high_price, close_price, date)



chromedriver.install()
chrome_options = webdriver.ChromeOptions()
wd = webdriver.Chrome(options=chrome_options)
wd.get('https://www.tgju.org/profile/price_dollar_rl/history')
wd.maximize_window() 
wd.implicitly_wait(20) 
crawler()
# conn = psycopg2.connect(host='localhost', database='data',
#                         user='ghazal', password='qwerty')

# cur = conn.cursor()
# cur.execute(
#     'CREATE TABLE prices (id SERIAL PRIMARY KEY, released_date DATE, closed_price INT);')
# cur.close()

# conn.close()
