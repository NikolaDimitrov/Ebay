import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import timeit


ebay_profile = []
df = pd.read_csv('EBAY-PAGE.csv')
url_products = df['User-URL']
url_products = list(dict.fromkeys(url_products))


def main_settings():
    start = timeit.default_timer()
    proxy = "196.244.200.54:12345"
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=' + proxy)
    options.add_argument('headless')
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    count = 0
    for url in url_products:
        count += 1
        print(count)
        print(url)
        settings_driver(url, driver)

    end = timeit.default_timer()
    print(end - start)
    make_csv_file()


def settings_driver(url, driver):
    driver.get(url)
    time.sleep(3)
    scrap_data(driver)


def scrap_data(driver):
    url_sale = driver.find_element_by_class_name('soi_lk').find_element_by_tag_name('a').get_attribute('href')
    driver.get(url_sale.replace("http", "https"))
    time.sleep(3)
    name_seller = driver.find_element_by_class_name('mbid').text
    tab = driver.find_elements_by_class_name('sresult')
    for item in tab:
        profile_data = {}
        profile_data['User'] = name_seller
        profile_data['URL'] = item.find_element_by_class_name('imgWr2').get_attribute('href')  
        profile_data['Title'] = item.find_element_by_class_name('vip').text  
        profile_data['Price'] = item.find_element_by_class_name('lvprice').text  
        try:
            profile_data['Condition'] = item.find_element_by_class_name('lvsubtitle').text
        except NoSuchElementException:
            profile_data['Condition'] = ''
        try:
            buy_action = item.find_element_by_class_name('lvformat').find_elements_by_tag_name('span')
            profile_data['Type of Purchase'] = buy_action[1].get_attribute('title')
        except IndexError:
            buy_action = item.find_element_by_class_name('lvformat').find_element_by_tag_name('span')
            profile_data['Type of Purchase'] = buy_action.text

        ebay_profile.append(profile_data)

def make_csv_file():
    df = pd.DataFrame(ebay_profile)
    df.to_csv('EBAY-PROFILE.csv', encoding='utf-8-sig', index=False)


main_settings()
