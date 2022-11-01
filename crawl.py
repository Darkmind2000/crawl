import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import mysql.connector
from bs4 import BeautifulSoup
import time
search_key=input("Enter Your Key for search:")
mydb = mysql.connector.connect(host='localhost',user='root',password='@Garshasp1',database='List')

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE ")
mycursor.execute("CREATE TABLE  DataScraping(Link VARCHAR(255), ProgrammingLanguage VARCHAR(20) , Stargazer VARCHAR(10))")
driver = webdriver.Firefox(executable_path="/home/blackclover/project/geckodriver")

r=driver.get('https://github.com')
driver.maximize_window()


test=driver.find_element(By.XPATH ,"/html/body/div[1]/header/div/div[2]/div/div/div[1]/div/div/form/label/input[1]")
test.send_keys(search_key+Keys.ENTER)

time.sleep(5)



#sql query set to var
sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer) VALUES (%s,%s,%s);"
val=("","","")
mycursor.execute(sql,val)
count=1
r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
    # Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')
res=int(soup.find('a',{"aria-label":"Page 100"}).text)
for x in range(res+1):
  #set search key in Url and rady to use in BeautifulSoup
  r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
  soup=BeautifulSoup(r.content,'html.parser')


  #find Links & Insert to Table mysql
  first_link = soup.find_all("a",{"class":"v-align-middle"})
  for i in first_link:
    p='https://github.com'+ str(i.get('href'))
    sql = "INSERT INTO DataScraping (Link) VALUES (%s)"

    mycursor.execute(sql,p)

  #Find Programmming Language & insert to Table mysql
  ProgramminfLanguage = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})

  for i in ProgramminfLanguage:
    k=i.select_one('span[itemprop="programmingLanguage"]')
    if (k == None ) :
        j='None'
        mycursor.execute("insert into DataScraping(ProgrammingLanguage) values(%s)", j)
    else:
        
        mycursor.execute("insert into DataScraping(ProgrammingLanguage) values(%s)", k.getText().lower())
  #Find Stargazer & Insert to Table mysql 
  star = soup.find_all("a" , {"class":"Link--muted"})
  for l in star:
    if ("issue" not in l.get_text().strip() ):
        print()
        mycursor.execute("insert into DataScraping(Stargazer) values(%s)", l.get_text().strip())
  count=count+1
  Bouton=driver.find_element(By.XPATH,'/html/body/div[4]/main/div/div[3]/div/div[2]/div/a[4]')
  Bouton.click()
time.sleep(10)
driver.quit()


