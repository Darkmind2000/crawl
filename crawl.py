from random import randint
import requests
# from seleniumwire import webdriver
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
import mysql.connector
from bs4 import BeautifulSoup
import time,datetime
from mechanize import Browser
search_key=input("Enter Your Key for search:")
mydb = mysql.connector.connect(host='localhost',user='root',password='@Garshasp1',database='List')
ts=datetime.datetime.now()
mycursor = mydb.cursor()
# mycursor.execute("CREATE DATABASE ")
mycursor.execute("CREATE TABLE IF NOT EXISTS SearchKey(Key_s VARCHAR(20), Date DATETIME)")
mycursor.execute("CREATE TABLE IF NOT EXISTS DataScraping(Link VARCHAR(255), ProgrammingLanguage VARCHAR(20) , Stargazer VARCHAR(10), Search_key VARCHAR(20))")
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
mycursor.execute("select Key_s from SearchKey")
id=mycursor.fetchall()

#sql query set to var
count=1
for item in id:
  if item[0] == search_key:
    print(item[0])
    res_user=input("#1_If you want to update: \n #2_If you want it to be displayed:")
    if res_user=="1":
      
      valu=(search_key,)
      mycursor.execute("DELETE FROM SearchKey WHERE Key_s=%s", valu)
      mydb.commit()
      mycursor.execute("DELETE FROM DataScraping WHERE Search_key=%s", valu)
      mydb.commit()
      sql="INSERT INTO SearchKey(Key_s,Date) VALUES (%s,%s);" 
      val=(search_key,ts)
      mycursor.execute(sql,val)
      
      r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
      # Parsing the HTML
      r.headers
      soup = BeautifulSoup(r.content, 'html.parser')
      res=soup.select_one('em[class="current"]')
      res1=int(res.get('data-total-pages'))
      for x in range(res1):
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
          
          q.insert(counter,p)
          # mycursor.execute(sql,(p,))
          counter=counter+1


        time.sleep(randint(3,6))
        #Find Programmming Language & insert to Table mysql
        ProgramminfLanguage = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
        w=[]
        counter=1
        for i in ProgramminfLanguage:
          k=i.select_one('span[itemprop="programmingLanguage"]')
          if (k == None ) :
            j='None'
            w.insert(counter,j)
          else:
            # print(counter)
            j=k.getText().lower()
            w.insert(counter,j)
          counter=counter+1
        time.sleep(randint(3,6))
        star = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
        e=[]
        counter=1 
        for l in star:
          l2=l.select_one('a[class="Link--muted"]')
          if(l2==None):
            l1='None'
            e.insert(counter,l1)
          else:
            l1 =l2.get_text().strip()
            # print(l1)
            e.insert(counter,l1)
          counter=counter+1
        res_error=r.status_code 
        if(res_error!=200):
          time.sleep(30)
          continue
        for z in range(10):
          # print(q[z])
          # print(w[z])
          # print(e[z])

          val=[q[z],w[z],e[z],search_key]
    
          sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer,Search_key) VALUES (%s,%s,%s,%s);"
          mycursor.executemany(sql,(val,))
          mydb.commit()
        val.clear()    
        count=count+1 
      time.sleep(randint(3,6)) 
    elif res_user=="2":
        mycursor.execute("SELECT Key_s,Date FROM SearchKey;")
        id=mycursor.fetchall()
        for item in id:
          print(item[0],"       " ,item[1])
        exit()

    
sql="INSERT INTO SearchKey(Key_s,Date) VALUES (%s,%s);"
val=(search_key,ts)
mycursor.execute(sql,val)
count=1
r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
# Parsing the HTML
r.headers
soup = BeautifulSoup(r.content, 'html.parser')
res=soup.select_one('em[class="current"]')
res1=int(res.get('data-total-pages'))

for x in range(res1):
          #set search key in Url and ready to use in BeautifulSoup
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
          # print(counter)
          # sql = "INSERT INTO DataScraping (Link) VALUES (%s)"
          q.insert(counter,p)
          # mycursor.execute(sql,(p,))
          counter=counter+1
    
  
        time.sleep(randint(2,6))
        #Find Programmming Language & insert to Table mysql
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
            # print(counter)
            j=k.getText().lower()
            w.insert(counter,j)
          counter=counter+1
        time.sleep(randint(2,6))
        #Find Stargazer & Insert to Table mysql 
        star = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
        e=[]
        counter=1 
        for l in star:
          l2=l.select_one('a[class="Link--muted"]')
          if(l2==None):
            l1='None'
            e.insert(counter,l1)
          else:
            l1 =l2.get_text().strip()
            # print(l1)
            e.insert(counter,l1)
          counter=counter+1
        res_error=r.status_code 
        if(res_error!=200):
          time.sleep(30)
          continue  
        for z in range(10):

          # print(q[z])
          # print(w[z])
          # print(e[z])
          val=[q[z],w[z],e[z],search_key]
     
          sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer,Search_key) VALUES (%s,%s,%s,%s);"
          mycursor.executemany(sql,(val,))
          mydb.commit()  
        val.clear()    
        count=count+1
        
  
time.sleep(randint(2,6))
# driver.quit()


