from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


google = []
url_list = ['https://www.google.com/search?rlz=1C1CHBD_enBG937BG937&biw=1366&bih=625&sxsrf=ALeKk03ceiWfFbrQ8cZ7NV2wnW_O1ZKJsQ%3A1613768676667&ei=5CcwYJOnKKSZlwSA8LtI&q=site%3Alinkedin.com%2Fin%2F+AND+industry%3AAutomotive+AND+location%3Anetherlands&oq=site%3Alinkedin.com%2Fin%2F+AND+industry%3AAutomotive+AND+location%3Anetherlands&gs_lcp=Cgdnd3Mtd2l6EANQAFgAYKRXaAFwAHgAgAGpAogBqQKSAQMyLTGYAQCqAQdnd3Mtd2l6wAEB&sclient=gws-wiz&ved=0ahUKEwiTqePl7PbuAhWkzIUKHQD4Dgk4ZBDh1QMIDQ&uact=5']


def main_settings():
    proxy = "196.244.200.54:12345"
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=' + proxy)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    for i in range(1, 3):
        url = url_list[-1]
        settings_driver(url, driver)

    make_csv_file()


def settings_driver(url, driver):
    driver.get(url)
    time.sleep(3)
    url_list.append(driver.find_element_by_class_name('pagination__next').get_attribute('href'))
    scrap_data(driver)


def scrap_data(driver):
    test = driver.find_elements_by_class_name("s-item")
# print(len(test))
    for i in test[1:]:
        table = {}
        table['Name'] = i.find_element_by_class_name('s-item__title').text    
        table['Price'] = i.find_element_by_class_name('s-item__price').text  
        table['URL of Picture'] = i.find_element_by_class_name('s-item__image-img').get_attribute('src')  
        try:
            buy_it = i.find_element_by_class_name('s-item__purchase-options-with-icon').text
            if buy_it == '':
                table['Type of Purchase'] = 'Buy/Offer'
            else:
                table['Type of Purchase'] = buy_it
        except NoSuchElementException:
            table['Type of Purchase'] = i.find_element_by_class_name('s-item__buyItNowOption').text    
        table['Hand'] = i.find_element_by_class_name('SECONDARY_INFO').text          
        table['Location'] = i.find_element_by_class_name('s-item__location').text      
        table['Delivery Price'] = i.find_element_by_class_name('s-item__logisticsCost').text      
        table['URL of Product'] = i.find_element_by_class_name('s-item__link').get_attribute('href')           

        ebay.append(table)


def make_csv_file():
    df = pd.DataFrame(ebay)
    df.to_csv('EBAY.csv', encoding='utf-8-sig', index=False)


main_settings()
