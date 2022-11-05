from random import randint
import requests
from seleniumwire import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import mysql.connector
from bs4 import BeautifulSoup
import time
from mechanize import Browser
search_key=input("Enter Your Key for search:")
mydb = mysql.connector.connect(host='localhost',user='root',password='@Garshasp1',database='List')

mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE ")
mycursor.execute("CREATE TABLE  DataScraping(Link VARCHAR(255), ProgrammingLanguage VARCHAR(20) , Stargazer VARCHAR(10))")
# driver = webdriver.Firefox(executable_path="/home/blackclover/project/geckodriver")

br=Browser()
br.set_handle_robots(False)
# r=driver.get('https://github.com')
# driver.maximize_window()

# for request in driver.requests:
#     # print(request.response.headers.add_header)
#     print(request.headers.get_all)
# test=driver.find_element(By.XPATH ,"/html/body/div[1]/header/div/div[2]/div/div/div[1]/div/div/form/label/input[1]")
# test.send_keys(search_key+Keys.ENTER)

time.sleep(randint(2,4))



#sql query set to var
# sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer) VALUES (%s,%s,%s);"
# val=("","","")
# mycursor.execute(sql,val)
count=1
r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
    # Parsing the HTML
r.headers
soup = BeautifulSoup(r.content, 'html.parser')
res=soup.select_one('em[class="current"]')
res1=int(res.get('data-total-pages'))

for x in range(res1+1):
  #set search key in Url and rady to use in BeautifulSoup
  br=Browser()
  br.set_handle_robots(False)
  br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
  r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
  soup=BeautifulSoup(r.content,'html.parser')
  

  #find Links & Insert to Table mysql
  q=[]
  counter=1
  first_link = soup.find_all("a",{"class":"v-align-middle"})
  for i in first_link:
    p='https://github.com'+ str(i.get('href'))
    print(counter)
    # sql = "INSERT INTO DataScraping (Link) VALUES (%s)"
    q.insert(counter,p)
    # mycursor.execute(sql,(p,))
    counter=counter+1
    
  
  time.sleep(randint(2,4))#Find Programmming Language & insert to Table mysql
  ProgramminfLanguage = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
  w=[]
  counter=1
  for i in ProgramminfLanguage:
    k=i.select_one('span[itemprop="programmingLanguage"]')
    if (k == None ) :
        j='None'
        # mycursor.execute("insert into DataScraping(ProgrammingLanguage) values(%s)", (j,))
        w.insert(counter,j)
    else:
        print(counter)
        j=k.getText().lower()
        w.insert(counter,j)
    counter=counter+1
    # mycursor.execute("insert into DataScraping(ProgrammingLanguage) values(%s)", (k.getText().lower(),))
  time.sleep(randint(2,4))
  #Find Stargazer & Insert to Table mysql 
  star = soup.find_all("a" , {"class":"Link--muted"})
  e=[]
  counter=1
  for l in star:
    if ("issue" not in l.get_text().strip() ):
        # print(counter)
        l1=l.get_text().strip()
        print(l1)
        e.insert(counter,l1)
    counter=counter+1
  print(r.status_code)  # mycursor.execute("insert into DataScraping(Stargazer) values(%s)", (l.get_text().strip(),))
  for z in range(10):

     print(q[z])
     print(w[z])
     print(e[z])

     val=[q[z],w[z],e[z]]
     
     sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer) VALUES (%s,%s,%s);"
     mycursor.executemany(sql,(val,))
     mydb.commit()  
  val.clear()    
  count=count+1
  # Bouton=driver.find_element(By.CSS_SELECTOR,'.next_page')
  # Bouton.click()
  
  time.sleep(randint(2,4))
# driver.quit()


