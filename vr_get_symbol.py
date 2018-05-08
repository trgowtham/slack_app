import requests
import selenium
from collections import namedtuple

from selenium import webdriver

driver_path = '/Users/nirmal/PycharmProjects/SD_scrapper/chromedriver'
driver = webdriver.Chrome(executable_path=driver_path)

POSTLOGINURL='https://www.valueresearchonline.com/'
driver.get(POSTLOGINURL)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
element = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "mob-search-input"))
    )


#driver.get ("https://www.valueresearchstocks.com/home/login")
print(element)
element1 = driver.find_element_by_id("mob-search-input")
print(element1.text)
element1.send_keys('PI Industries')
driver.find_element_by_id("mob-search-btn").click()
html_page = driver.page_source
#driver.close()

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_page, 'html.parser')
print(soup)
#element.send_keys('PI Industries\n')
#element.submit()
#driver.find_element_by_id("password").send_keys("handl3bar")
#driver.find_element_by_id("mob-search-btn").click()
#res = driver.find_element_by_class_name('input')
#print(res)
#frame = driver.find_elements_by_class_name("iframe")
#print(frame)
#src = frame.get_attribute('src')
#print(dir(driver))
#driver.implicitly_wait(3)

#print (post)
#driver.close()