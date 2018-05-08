import requests
import selenium
from collections import namedtuple

from selenium import webdriver

driver_path = '/Users/nirmal/PycharmProjects/SD_scrapper/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)

POSTLOGINURL='https://www.valueresearchonline.com/membership/getin.asp'
driver.get(POSTLOGINURL)
#driver.get ("https://www.valueresearchstocks.com/home/login")

driver.find_element_by_id("username").send_keys('kuchbivr@gmail.com')
driver.find_element_by_id("password").send_keys("handl3bar")
driver.find_element_by_id("submitbtn").click()
#res = driver.find_element_by_class_name('input')
#print(res)
#frame = driver.find_elements_by_class_name("iframe")
#print(frame)
#src = frame.get_attribute('src')
#print(dir(driver))
driver.implicitly_wait(3)
driver.get('https://www.valueresearchstocks.com/recos-all')
driver.implicitly_wait(2)
html_page = driver.page_source
#driver.close()

# save html page to file
f = open('html_page', 'w')
f.writelines(html_page)
f.close()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_page, 'html.parser')
#print(soup)
#for offer in soup.find_all('span', attrs={'class': 'label label-success'}):
#    print (offer.parent.text)
#for timely in soup.find_all('span',attrs={'class': 'label label-primary'}):
#    print (timely.parent.text)
recos = []
rows = soup.find_all('tr', attrs={'class': ['odd', 'even']})
print (rows[0])
#import pdb;pdb.set_trace()
f_row = rows[0]
str = f_row.find_all('a', attrs={'class': "center-block"})[0]
stock_code = str['href'].split('/')[2]
stock_url = 'https://www.valueresearchonline.com/stocks/snapshot.asp?code=' + stock_code
print(stock_url)
driver.get(stock_url)
stock_page = driver.page_source
#print(stock_page)
soup1 = BeautifulSoup(stock_page, 'html.parser')
print(soup1.find(lambda tag:tag.name=="td" and "NSE Code:" in tag.text).text.split(":"))

import  sys;sys.exit()
#for rows in soup.find_all('tr', attrs={'class': ['odd', 'even']}):
#    print(r
    #cells = rows.findAll('td')
    #print(cells[0])
    #reco = [c for c in cells]
    #recos.append(reco)

#from tinydb import TinyDB, Query
# #db = TinyDB('db.json')

#from tinydb import Query
#User = Query()

#test = namedtuple('Stock', 'reco_date, name')

#for reco in recos:
#    print(reco)
#    if len(reco) > 1:
#        if not db.contains(User.name == reco[1]):
#            db.insert({'date': reco[0], 'name': reco[1]})



#for item in db:
#    print(item)


#db.purge()

#print(len(db))

#import  time;time.sleep(120)


#payload = {'username': 'kuchbivr@gmail.com', 'password': 'handl3bar'}

#REQUESTURL = 'https://www.valueresearchstocks.com/recos-all'
#with requests.Session() as session:
#   post = session.post(POSTLOGINURL, data=payload)
#   r = session.get(REQUESTURL)
   #print(r.text)
   #print (post)