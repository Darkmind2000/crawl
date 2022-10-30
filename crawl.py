import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import mysql.connector
from bs4 import BeautifulSoup
import time
search_key=input("Enter Your Key for search:")
# mydb = mysql.connector(host='localhost',user='root',password='123456')

# mycursor = mydb.cursor()
# mycursor = execute("CREATE DATABASE List")

driver = webdriver.Firefox(executable_path="/home/blackclover/project/geckodriver")

r=driver.get('https://github.com')
driver.maximize_window()


test=driver.find_element(By.XPATH ,"/html/body/div[1]/header/div/div[2]/div/div/div[1]/div/div/form/label/input[1]")
test.send_keys(search_key+Keys.ENTER)

time.sleep(5)


r=requests.get('https://github.com/search?q={}&type=Repositories'.format(search_key))
print(r)
soup=BeautifulSoup(r.content,'html.parser')

list_link=[]

first_link = soup.find_all("a",{"class":"v-align-middle"})
print(first_link)
for i in first_link:
    if "href" in first_link:
        list_link=first_link


# while(True):
#     table1=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[1]/div[2]/div[1]/div/a")
#     val.append(table1) 
#     t=table1.click()
#     x.append(t)
#     table2=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[2]/div[2]/div[1]/div/a")
#     val.append(table2)
#     table3=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[3]/div[2]/div[1]/div/a")
#     val.append(table3)
#     table4=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[4]/div[2]/div[1]/div/a")
#     val.append(table4)
#     table5=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[5]/div[2]/div[1]/div/a")
#     val.append(table5)
#     table6=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[6]/div[2]/div[1]/div/a")
#     val.append(table6)
#     table7=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[7]/div[2]/div[1]/div/a")
#     val.append(table7)
#     table8=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[8]/div[2]/div[1]/div/a")
#     val.append(table8)
#     table9=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[9]/div[2]/div[1]/div/a")
#     val.append(table9)
#     table10=driver.find_element(By.XPATH,"/html/body/div[4]/main/div/div[3]/div/ul/li[10]/div[2]/div[1]/div/a")
#     val.append(table10)
    
#     if(soup.find(attrs="next_page disabled")):
#         break
#     elif("/html/body/div[4]/main/div/div[3]/div/div[3]/div/a[7]"):
#         t=driver.find_element(By.XPATH , "/html/body/div[4]/main/div/div[3]/div/div[3]/div/a[7]")
#         t.click()
#     time.sleep(10)
# sql="INSERT INTO List (Link) VALUES (%s);"

# mycursor.executemany(sql,val)
# val[0].click()
print(list_link)
time.sleep(10)


