import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException   
options = Options()
#chrome_options.add_argument("--headless")
options.add_argument("--incognito")
options.add_argument("--window-size=1280x1696")

# Global Variables
chrome = webdriver.Chrome(("chromedriver"), options=options)


def get_cookie() -> str:
    """
    This function gets a cookie for use
    when making requests

    :return: the cookie
    :rtype: str

    """
    chrome.get("https://www.forbes.com/billionaires")
    chrome.find_element(By.XPATH, '//*[@id="truste-consent-button"]').click()
    cookies = chrome.get_cookies()
    cookie_for_requests = cookies[4]['value']
    chrome.close()
    return cookie_for_requests


def req_with_cookie(cookie_for_requests):
    """
    This function makes a request with a
    cookie

    :param str cookie_for_requests: this is a cookie which enables us to make requests to the endpoint
    :return: contents of the api response
    :rtype: dict

    """
    cookies = dict(
        Cookie=f'notice_preferences=2:; notice_gdpr_prefs=0,1,2::implied,eu; euconsent-v2={cookie_for_requests};')
    r = requests.get("https://www.forbes.com/billionaires/page-data/index/page-data.json", cookies=cookies)
    return r.json()


if __name__ == '__main__':
    data = req_with_cookie(get_cookie())
    for row in range(10):
        print(data['result']['pageContext']['tableData'][row]['employment']['name'])
