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
#CONNECT SQL
mydb = mysql.connector.connect(host='localhost',user='root',password='@Garshasp1',database='List')
#tarikh alan ra migirad
ts=datetime.datetime.now()
print("sql connect")
mycursor = mydb.cursor()
#table searchkey ke tarikh va searchk_key ra darad sakhte mishavad
mycursor.execute("CREATE TABLE IF NOT EXISTS SearchKey(Key_s VARCHAR(20), Date DATETIME)")
#table DataScraping ke tamame data ra negah dari mikonad sakhte mi shavad
mycursor.execute("CREATE TABLE IF NOT EXISTS DataScraping(Link VARCHAR(255), ProgrammingLanguage VARCHAR(20) , Stargazer VARCHAR(10), Search_key VARCHAR(20))")


br=Browser()
#robot.txt site ra pak mikonad
br.set_handle_robots(False)
#func update : agar search_key mojood bashe va user bekhahad be roz shavad tamame search  gozashte dar mode search_key ra pak mikonad va dobare vared mikonad
def Update(search_key):
    count=1
    valu=(search_key,)
    #table Searchkey word morede nazar ra pak mikonad
    mycursor.execute("DELETE FROM SearchKey WHERE Key_s=%s", valu)
    mydb.commit()
    #table DataScraping word morede nazar ra pak mikonad
    mycursor.execute("DELETE FROM DataScraping WHERE Search_key=%s", valu)
    mydb.commit()
    #table SearchKey value ha ra save mikonad 
    sql="INSERT INTO SearchKey(Key_s,Date) VALUES (%s,%s);" 
    val=(search_key,ts)
    mycursor.execute(sql,val)
    #site page ra migirad
    r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
    # Parsing the HTML
    soup = BeautifulSoup(r.content, 'html.parser')
    #tedade safahate mojood az search_key ra be dast miavarad
    res=soup.select_one('em[class="current"]')
    res1=int(res.get('data-total-pages'))
    for x in range(res1):
      #set search key in Url and ready to use in BeautifulSoup
      br=Browser()
      #robot.txt site ra pak mikonad
      br.set_handle_robots(False)
      #taghire header
      br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
      r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
      soup=BeautifulSoup(r.content,'html.parser')
      #find Links 
      q=[]
      counter=1
      first_link = soup.find_all("a",{"class":"v-align-middle"})
      for i in first_link:
        p='https://github.com'+ str(i.get('href'))
        
        q.insert(counter,p)
        counter=counter+1


      time.sleep(randint(3,6))
      #Find Programmming Language 
      ProgramminfLanguage = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
      w=[]
      counter=1
      for i in ProgramminfLanguage:
        k=i.select_one('span[itemprop="programmingLanguage"]')
        if (k == None ) :
          j='None'
          w.insert(counter,j)
        else:
          j=k.getText().lower()
          w.insert(counter,j)
        counter=counter+1
      time.sleep(randint(3,6))
      #Find Stargazer of Links searching
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
          e.insert(counter,l1)
        counter=counter+1
      res_error=r.status_code 
      if(res_error!=200):
        time.sleep(30)
        continue
      #Insert  Links,ProgrammingLanguage,Sratgazer to Table mysql
      for z in range(10):
        val=[q[z],w[z],e[z],search_key]
        sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer,Search_key) VALUES (%s,%s,%s,%s);"
        mycursor.executemany(sql,(val,))
        mydb.commit()
      #khali kardane list value ha ta dobare dar page ba'adi jadid ha ra vared konad 
      val.clear()    
      count=count+1 
    time.sleep(randint(3,6)) 
#func Display: show value and date of page's search  
def Display():
  mycursor.execute("SELECT Key_s,Date FROM SearchKey;")
  id=mycursor.fetchall()
  for item in id:
    print(item[0],"       " ,item[1])
  exit()
#func New_Search: search_key jadid ra search mikonad va dar table ha save mikonad
def New_Search(search_key):
  #table SearchKey value ha ra save mikonad
  sql="INSERT INTO SearchKey(Key_s,Date) VALUES (%s,%s);"
  val=(search_key,ts)
  mycursor.execute(sql,val)
  count=1
  #site page ra migirad
  r=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
  # Parsing the HTML
  soup = BeautifulSoup(r.content, 'html.parser')
  #tedade safahate mojood az search_key ra be dast miavarad 
  res=soup.select_one('em[class="current"]')
  if(res!=None):
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
          q.insert(counter,p)
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
            w.insert(counter,j)
          else:
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
            e.insert(counter,l1)
          counter=counter+1
        #agar status_code 200 bashad accept hast dar gheyer in sorat dobare 30s sabr mikonad va dobare search ra edame midahad
        res_error=r.status_code 
        if(res_error!=200):
          time.sleep(30)
          continue  
        #Insert  Links,ProgrammingLanguage,Sratgazer to Table mysql
        for z in range(10):
          val=[q[z],w[z],e[z],search_key]
          sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer,Search_key) VALUES (%s,%s,%s,%s);"
          mycursor.executemany(sql,(val,))
          mydb.commit()  
        val.clear()    
        count=count+1
  #agar word dorost nabashad error midahad
  else:
    print("****Please search for the correct word****")         
  time.sleep(randint(2,6))

time.sleep(randint(2,4))
#tamame search_key haye gozashte ra biroon miavarad 
mycursor.execute("select Key_s from SearchKey")
id=mycursor.fetchall()
#func  RUN: barresimokonad search_key jadid agar bood update ya display konad , agar nabood save konad 
def RUN(search_key,id):
  # sql query set to var
  for item in id:
    if item[0] == search_key:
      print(item[0])
      res_user=input("#1_If you want to update: \n #2_If you want it to be displayed:")
      if res_user=="1":
        Update(search_key)
      elif res_user=="2":
        Display()
    else:
        New_Search(search_key)
        

RUN(search_key,id)
