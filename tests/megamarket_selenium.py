from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

browser = webdriver.Firefox()
browser.set_page_load_timeout(3)
delay = 3 # seconds
try:
    browser.get("https://megamarket.ru/catalog/noutbuki/")
    myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print("Page is ready!")
except TimeoutException:
    print(browser.find_element(By.TAG_NAME, "body").text)
    print("Loading took too much time!")