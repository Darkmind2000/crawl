from distutils.util import execute
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import mysql.connector
from bs4 import BeautifulSoup
import time
search_key=input("Enter Your Key for search:")
mydb = mysql.connector(host='localhost',user='root',password='123456')

mycursor = mydb.cursor()
mycursor = execute("CREATE DATABASE List")

driver = webdriver.Firefox(executable_path="/home/blackclover/project/geckodriver")

r=driver.get('https://github.com')
driver.maximize_window()


test=driver.find_element(By.XPATH ,"/html/body/div[1]/header/div/div[2]/div/div/div[1]/div/div/form/label/input[1]")
test.send_keys(search_key+Keys.ENTER)

time.sleep(5)


r=requests.get('https://github.com/search?q={}&type=Repositories'.format(search_key))
soup=BeautifulSoup(r.content,'html.parser')

first_link = soup.find_all("a",{"class":"v-align-middle"})
for i in first_link:
    print(i.get('href'))

#sql query set to var
sql="INSERT INTO List (Link,Star,ProgrammingLanguage ) VALUES (%s,%s,%s);"
val=("","","")
mycursor.executemany(sql,val)
ProgramminfLanguage = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})

for i in ProgramminfLanguage:
    k=i.select_one('span[itemprop="programmingLanguage"]')
    if (k == None ) :
        j='None'
        print(j)
    else:
        print(k.getText())


star = soup.find_all("a" , {"class":"Link--muted"})
for j in star:
    if ("issue" not in j.get_text().strip() ):
        print(j.get_text().strip())

# programing_language = soup.find_all('span' , {"itemprop":"programmingLanguage"})
# for k in programing_language:
#     if (k.get_text().strip() == " "):
#         print("Null")
#     else:
#         print(k.get_text().strip())
time.sleep(10)
driver.quit()


