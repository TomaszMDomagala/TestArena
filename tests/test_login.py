from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# from resources.logger import get_logger
from resources.utils import extract_data
# from resources.exceptions import IncorectLoginData, PageNotLoaded

import pytest
import time

@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        driver.get("http://testarena.pl/demo")
        yield driver
        driver.quit()

def test_login(driver):
    description = driver.find_element(By.CLASS_NAME, "description")
    items = description.find_elements(By.TAG_NAME, 'p')
    login, password = extract_data(items[0].text)
    demo_button = items[1].find_element(By.TAG_NAME, 'a')

    demo_button.click()

    login_page = driver.switch_to.window(driver.window_handles[1])
    print(login_page)
    time.sleep(2)

    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(login)
    pass_input = driver.find_element(By.ID, "password")
    pass_input.send_keys(password)
    driver.find_element(By.ID, "login").click()
