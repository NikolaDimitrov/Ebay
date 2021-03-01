import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
import timeit


ebay_page = []
df = pd.read_csv('EBAY.csv')
url_products = df['URL of Product']


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
    time.sleep(5)
    scrap_data(driver)


def scrap_data(driver):
    page_data = {}
    try:
        page_data['Title'] = driver.find_element_by_class_name('it-ttl').text
    except NoSuchElementException:
        page_data['Title'] = driver.find_element_by_class_name("product-title").text
    # <span class="notranslate" id="prcIsum" itemprop="price" style="" content="475.0">£475.00</span>
    try:
        try:
            page_data['Price'] = driver.find_element_by_id("prcIsum").text
        except NoSuchElementException:
            page_data['Price'] = driver.find_element_by_id("mm-saleDscPrc").text
    except NoSuchElementException:
        page_data['Price'] = driver.find_elements_by_class_name('display-price')
    # <div class="u-flL condText  " id="vi-itm-cond" itemprop="itemCondition">Seller refurbished</div>
    try:
        page_data['Condition'] = driver.find_element_by_id('vi-itm-cond').text
    except NoSuchElementException:
        condition = driver.find_elements_by_class_name("cc-ts-BOLD")
        page_data['Condition'] = condition[1].text
    try:
        user = driver.find_element_by_class_name("mbg").find_element_by_tag_name('a')
        page_data['User-URL'] = user.get_attribute('href')
    except NoSuchElementException:
        user = driver.find_element_by_class_name("seller-persona ").find_element_by_tag_name('a')
        page_data['User-URL'] = user.get_attribute('href')
    # <div id="desc_wrapper_ctr">
    try:
        iframe = driver.find_element_by_tag_name('iframe')
        driver.switch_to.frame(iframe)
        description = driver.find_element_by_tag_name('div')
        page_data['Description'] = description.text.replace("\n", "(NL)")
    except NoSuchElementException:
        driver.switch_to.default_content()
        description = driver.find_element_by_class_name('spec-row')
        page_data['Description'] = description.text.replace("\n", "(NL)")

    ebay_page.append(page_data)


def make_csv_file():
    df = pd.DataFrame(ebay_page)
    df.to_csv('EBAY-PAGE.csv', encoding='utf-8-sig', index=False)


main_settings()
