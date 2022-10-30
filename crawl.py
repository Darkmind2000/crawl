import requests
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import mysql.connector
search_key=input("Enter Your Key for search:")
mydb = mysql.connector(host='localhost',user='root',password='123456')

mycursor = mydb.cursor()
mycursor = execute("CREATE DATABASE List")

driver = webdriver.Firefox(executable_path="/home/blackclover/project/geckodriver")

driver.get('https://github.com')
driver.maximize_window()

test=driver.find_element(By.XPATH ,"/html/body/div[1]/header/div/div[2]/div/div/div[1]/div/div/form/label/input[1]")
test.send_keys(search_key+Keys.ENTER)


val=[]
while(True):
    for i in range(1,11):
        table=driver.find_element(By.XPATH, "/html/body/div[4]/main/div/div[3]/div/ul/li[{}]/div[2]/div[1]/div/a")
        val.append(table.format(i))  
    if("/html/body/div[4]/main/div/div[3]/div/div[3]/div/span[2]"):
        break
    elif("/html/body/div[4]/main/div/div[3]/div/div[3]/div/a[7]"):
        t=driver.find_element(By.XPATH , "/html/body/div[4]/main/div/div[3]/div/div[3]/div/a[7]")
        t.click()

sql="INSERT INTO List (Link) VALUES (%s);"

mycursor.executemany(sql,val)

time.sleep(10)


