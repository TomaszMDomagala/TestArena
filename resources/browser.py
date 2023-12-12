from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from resources.logger import get_logger
from resources.utils import extract_data
from resources.exceptions import IncorectLoginData, PageNotLoaded

import pytest
import re
import sys
import time


logger = get_logger(__name__)


@pytest.fixture
def driver(request):
    url = request.param
    options = Options()
    # options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        yield driver
        driver.quit()


@pytest.fixture
def logged_in_driver(request):
    options = Options()
    # options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        driver.get("http://demo.testarena.pl/logowanie")
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(request.param['login'])
        pass_input = driver.find_element(By.ID, "password")
        pass_input.send_keys(request.param['password'])
        driver.find_element(By.ID, "login").click()
        yield driver
        driver.quit()


# def wait_until_element_is_loaded(driver, locator: By, element: str):
#     try:
#         elem = WebDriverWait(driver, 30).until(
#             EC.presence_of_element_located((locator, element))
#         )
#     except PageNotLoaded as e:
#         logger.error("Exception occurred: ", e)
