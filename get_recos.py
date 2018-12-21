# Tasks
#
# Do login
# get recommendation page
# for each reco extrat stock id on VR website
# get stock page and extract NSE code
import os

from bs4 import BeautifulSoup
from selenium import webdriver


from stocks import Stock, check_stock_in_db, add_recos

DRIVER_PATH='/chromedriver'
VR_LOGIN_URL='https://www.valueresearchonline.com/membership/getin.asp'
VR_USERNAME='kuchbivr@gmail.com'
VR_PASSWORD='handl3bar'
VR_ALL_RECO_URL='https://www.valueresearchstocks.com/recos-all'

#Append stock code to get VR stock page
VR_STOCK_URL='https://www.valueresearchonline.com/stocks/snapshot.asp?code='

driver_path = os.path.dirname(os.path.realpath(__file__)) + DRIVER_PATH
print(driver_path)
driver = webdriver.Chrome(executable_path=driver_path)


def login_vr():
    '''
    Login to VR page
    :param driver:
    :return: None
    '''
    driver.get(VR_LOGIN_URL)
    #TODO improve how we wait for page loading
    driver.implicitly_wait(3)
    # provide login id and password
    driver.find_element_by_id("username").send_keys('kuchbivr@gmail.com')
    driver.find_element_by_id("password").send_keys("handl3bar")
    driver.find_element_by_id("submitbtn").click()

def get_html(url):
    '''
    Returns html contents of url

    :param driver:  webriver
    :param url: url to download
    :return:  html contents of
    '''
    driver.get(url)
    return driver.page_source

def process_recos_html(reco_elements):
    '''
    Input is of type bs4.element.ResultSet.
    Each element represents one stock in reco table
    which needs to be converted to Stock object and
    stored in DB
    :param reco_elements:
    :return:
    '''


    # record new recos encountered
    new_recos = []

    for row in reco_elements:
        cells = list(row.find_all('td'))
        # Sample row

    # 0: <td>
    # <a href="/stocks/296/ashiana-housing-ltd#premium-coverage">
    #                                                         Ashiana Housing                                                    </a>
    # <small class="text-capitalize drkgrey"></small> </td>
    # 1: <td data-order="20171027" width="8%">
    #                                                     27-Oct-17                                                </td>
    # 2: <td class="text-right">166.70</td>
    # 3: <td class="text-right">147.25</td>
    # 4: <td class="text-right" width="">-11.7</td>
    # 5: <td class="text-right" width="">3.5</td>
    # 6: <td class="text-right">1,520</td>
    # 7: <td class="text-right ">39.77</td>
    # 8: <td class="text-right ">1.99</td>
    # 9: <td class="text-right">24/30</td>
    # 10: <td class="text-center text-right"><a class="text-uppercase view-coverage" href="/coverage?company_code=296">view</a></td>
    # 11: <td class="text-center text-right">
    # <a class="text-uppercase add-watchlist" href="#"> added </a>
    # </td>
        if len(cells) < 2:
            # not a valid row
            break

        reco_date = cells[1].text.strip()
        # Extract name and stock_id from 1st cell
        reco_name = cells[0].text.strip()

        if '\n' in reco_name:
            stock_name, stock_type = reco_name.split('\n')
            stock_name = stock_name.strip()
            stock_type = stock_type.strip()
        else:
            stock_name = reco_name
            stock_type = 'NA'

        # extract href

        href = cells[0].find_all('a')[0]['href']

        vr_code = href.rsplit('/')[2]
        stock_symbol = get_symbol(vr_code)
        # Timely or All-weather -- this can be missing.
        #stock_type = row.find()
        print(f' {stock_name},{stock_type}, {stock_symbol}')

        # cells[2] -- market cap not required right now
        reco_date_price = cells[3].text.strip()

        print(f" 2: {cells[2].text}")
        print(f" 3: {cells[3].text}")
        #(self, name, type, symbol, reco_date, reco_date_price, stock_id)
        # create a stock object check if it exists in db if not add.

        if not check_stock_in_db(stock_symbol):
            stock = Stock(stock_name, stock_type, stock_symbol,reco_date, reco_date_price, vr_code)
            new_recos.append(stock)

    # add_recos to the csv file
    add_recos(new_recos)
    print(f"Saved {len(new_recos)}")
    #TODO Send alert for new recos added using list new_recos

    return

def get_symbol(vr_code):

    stock_url = VR_STOCK_URL + vr_code
    print(f'get_symbol: {stock_url}')
    driver.get(stock_url)
    stock_page = driver.page_source
    # print(stock_page)
    soup = BeautifulSoup(stock_page, 'html.parser')
    stock_symbol = soup.find(lambda tag: tag.name == "td" and "NSE Code:" in tag.text).text.split(":")
    return stock_symbol[1].strip()

def main():


    # login to VR
    login_vr()
    # wait for login to complete
    driver.implicitly_wait(3)
    print("Login successful")
    # get all recos
    all_reco_html = get_html(VR_ALL_RECO_URL)
    #f = open('html_page', 'r')
    #all_reco_html = ''.join(f.readlines())
    soup = BeautifulSoup(all_reco_html, 'html.parser')
    reco_rows = soup.find_all('tr', attrs={'class': ['odd', 'even']})

    # process all recos
    process_recos_html(reco_rows)
    driver.close()


if __name__ == '__main__':
    main()
