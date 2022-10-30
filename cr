import os 
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
search_key=input("Enter Your Key for search:")

# path=os.path.dirname(os.path.abspath(__file__))
# address=os.path.join(path,'geckodriver')
# driver = webdriver.Firefox(executable_path="./home/project/geckodriver")
driver = webdriver.Firefox()

driver.get('https://github.com')
driver.maximize_window()

test=driver.find_element_by_css_selector(".js-site-search-focus")
test.send_key(search_key + Keys.ENTER)

find_link= driver.find_element(By.ID , 'f4 text-normal')
time.sleep(10)


