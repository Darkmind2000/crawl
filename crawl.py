from random import randint
import requests
import mysql.connector
from bs4 import BeautifulSoup
import time,datetime
from mechanize import Browser

def update(search_key):
    count=1
    value_search_key=(search_key,)
    #table Searchkey word morede nazar ra pak mikonad
    mycursor.execute("DELETE FROM SearchKey WHERE Key_s=%s", value_search_key)
    #table DataScraping word morede nazar ra pak mikonad
    mycursor.execute("DELETE FROM DataScraping WHERE Search_key=%s", value_search_key)
    mydb.commit()
    #table SearchKey value ha ra save mikonad 
    sql="INSERT INTO SearchKey(Key_s,Date) VALUES (%s,%s);" 
    val=(search_key,take_time_now)
    mycursor.execute(sql,val)
    #site page ra migirad
    web_pageـdesired=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
    # Parsing the HTML
    soup = BeautifulSoup(web_pageـdesired.content, 'html.parser')
    #tedade safahate mojood az search_key ra be dast miavarad
    number_page=int(soup.select_one('em[class="current"]').get('data-total-pages'))
    
    for counter_number_page in range(number_page):
      
      #robot.txt site ra pak mikonad
      browser.set_handle_robots(False)
      #taghire header
      browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
      web_pageـdesired=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
      soup=BeautifulSoup(web_pageـdesired.content,'html.parser')
      #find Links 
      list_link_found=[]
      counter=1
      links = soup.find_all("a",{"class":"v-align-middle"})
      for counter_for_links in links:
        complete_link='https://github.com'+ str(counter_for_links.get('href'))
        
        list_link_found.insert(counter,complete_link)
        counter=counter+1


      time.sleep(randint(3,6))
      #Find Programmming Language 
      programminglanguage_tag = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
      list_programinglanguage=[]
      counter=1
      for counter_programinglanguage_tag in programminglanguage_tag:
        select_every_programminglanguage=counter_programinglanguage_tag.select_one('span[itemprop="programmingLanguage"]')
        if (select_every_programminglanguage == None ) :
          setting_programminglanguage='None'
          list_programinglanguage.insert(counter,setting_programminglanguage)
        else:
          setting_programminglanguage=select_every_programminglanguage.getText().lower()
          list_programinglanguage.insert(counter,setting_programminglanguage)
        counter=counter+1
      time.sleep(randint(3,6))
      #Find Stargazer of Links searching
      all_star_tags = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
      list_stargazer=[]
      counter=1 
      for counter_for_all_star_tags in all_star_tags:
        select_every_star=counter_for_all_star_tags.select_one('a[class="Link--muted"]')
        if(select_every_star==None):
          setting_star='None'
          list_stargazer.insert(counter,setting_star)
        else:
          setting_star =select_every_star.get_text().strip()
          list_stargazer.insert(counter,setting_star)
        counter=counter+1
      result_error=web_pageـdesired.status_code 
      if(result_error!=200):
        time.sleep(30)
        continue
      #Insert  Links,ProgrammingLanguage,Sratgazer to Table mysql
      for counter_pages in range(10):
        val=[list_link_found[counter_pages],list_programinglanguage[counter_pages],list_stargazer[counter_pages],search_key]
        sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer,Search_key) VALUES (%s,%s,%s,%s);"
        mycursor.executemany(sql,(val,))
        mydb.commit()
      #khali kardane list value ha ta dobare dar page ba'adi jadid ha ra vared konad 
      val.clear()    
      count=count+1 
    time.sleep(randint(3,6)) 
#func Display: show value and date of page's search  
def display():
  mycursor.execute("SELECT Key_s,Date FROM SearchKey;")
  id=mycursor.fetchall()
  for item in id:
    print(item[0],"       " ,item[1])
  exit()
#func New_Search: search_key jadid ra search mikonad va dar table ha save mikonad
def new_search(search_key):
  #table SearchKey value ha ra save mikonad
  sql="INSERT INTO SearchKey(Key_s,Date) VALUES (%s,%s);"
  val=(search_key,take_time_now)
  mycursor.execute(sql,val)
  count=1
  #site page ra migirad
  web_pageـdesired=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
  # Parsing the HTML
  soup = BeautifulSoup(web_pageـdesired.content, 'html.parser')
  #tag haye marboot be tedade safahat ra search mikonad va agar mojood bood tedad ra be dast miavarad
  number_page_tags=soup.select_one('em[class="current"]')
  if(number_page_tags!=None):
    #tedade safahate mojood az search_key ra be dast miavarad 
    number_page=int(number_page_tags.get('data-total-pages'))
    for counter_number_page in range(number_page):
        #set search key in Url and ready to use in BeautifulSoup

        browser.set_handle_robots(False)
        browser.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36')]
        web_pageـdesired=requests.get('https://github.com/search?p={}&q={}&type=Repositories'.format(count,search_key))
        soup=BeautifulSoup(web_pageـdesired.content,'html.parser')
        #find Links & Insert to Table mysql
        list_link_found=[]
        counter=1
        links = soup.find_all("a",{"class":"v-align-middle"})
        for counter_for_links in links:
          complete_link='https://github.com'+ str(counter_for_links.get('href'))
          list_link_found.insert(counter,complete_link)
          counter=counter+1
        time.sleep(randint(2,6))
        #Find Programmming Language & insert to Table mysql
        programminglanguage_tag = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
        list_programinglanguage=[]
        counter=1
        for counter_programinglanguage_tag in programminglanguage_tag:
          select_every_programminglanguage=counter_programinglanguage_tag.select_one('span[itemprop="programmingLanguage"]')
          if (select_every_programminglanguage == None ) :
            setting_programminglanguage='None'
            list_programinglanguage.insert(counter,setting_programminglanguage)
          else:
            setting_programminglanguage=select_every_programminglanguage.getText().lower()
            list_programinglanguage.insert(counter,setting_programminglanguage)
          counter=counter+1
        time.sleep(randint(2,6))
        #Find Stargazer & Insert to Table mysql 
        all_star_tags = soup.find_all('li', {"class":"repo-list-item hx_hit-repo d-flex flex-justify-start py-4 public source"})
        list_stargazer=[]
        counter=1 
        for counter_for_all_star_tags in all_star_tags:
          select_every_star=counter_for_all_star_tags.select_one('a[class="Link--muted"]')
          if(select_every_star==None):
            setting_star='None'
            list_stargazer.insert(counter,setting_star)
          else:
            setting_star =select_every_star.get_text().strip()
            list_stargazer.insert(counter,setting_star)
          counter=counter+1
        #agar status_code 200 bashad accept hast dar gheyer in sorat dobare 30s sabr mikonad va dobare search ra edame midahad
        result_error=web_pageـdesired.status_code 
        if(result_error!=200):
          time.sleep(30)
          continue  
        #Insert  Links,ProgrammingLanguage,Sratgazer to Table mysql
        for counter_pages in range(10):
          val=[list_link_found[counter_pages],list_programinglanguage[counter_pages],list_stargazer[counter_pages],search_key]
          sql="INSERT INTO DataScraping (Link,ProgrammingLanguage,Stargazer,Search_key) VALUES (%s,%s,%s,%s);"
          mycursor.executemany(sql,(val,))
          mydb.commit()  
        val.clear()    
        count=count+1
  #agar word dorost nabashad error midahad
  else:
    print("****Please search for the correct word****")         
  time.sleep(randint(2,6))


#func  RUN: barresimokonad search_key jadid agar bood update ya display konad , agar nabood save konad 
def run(search_key,id):
  # sql query set to var
  for item in id:
    if item[0] == search_key:
      print(item[0])
      res_user=input("#1_If you want to update: \n #2_If you want it to be displayed:")
      if res_user=="1":
        update(search_key)
      elif res_user=="2":
        display()
    else:
        new_search(search_key)

search_key=input("Enter Your Key for search:")
#CONNECT SQL
mydb = mysql.connector.connect(host='localhost',user='root',password='@Garshasp1',database='List')
#tarikh alan ra migirad
take_time_now=datetime.datetime.now()
print("sql connect")
mycursor = mydb.cursor()
#table searchkey ke tarikh va searchk_key ra darad sakhte mishavad
mycursor.execute("CREATE TABLE IF NOT EXISTS SearchKey(Key_s VARCHAR(20), Date DATETIME)")
#table DataScraping ke tamame data ra negah dari mikonad sakhte mi shavad
mycursor.execute("CREATE TABLE IF NOT EXISTS DataScraping(Link VARCHAR(255), ProgrammingLanguage VARCHAR(20) , Stargazer VARCHAR(10), Search_key VARCHAR(20))")
browser=Browser()
#robot.txt site ra pak mikonad
browser.set_handle_robots(False)
#func update : agar search_key mojood bashe va user bekhahad be roz shavad tamame search  gozashte dar mode search_key ra pak mikonad va dobare vared mikonad        
time.sleep(randint(2,4))
#tamame search_key haye gozashte ra biroon miavarad 
mycursor.execute("select Key_s from SearchKey")
id=mycursor.fetchall()
run(search_key,id)
