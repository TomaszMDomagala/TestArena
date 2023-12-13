from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC

from typing import Union

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
    options.add_argument("-private")
    with webdriver.Firefox(options=options) as driver:
        driver.get(url)
        yield driver
        driver.quit()


@pytest.fixture
def logged_in_driver(request):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("-private")
    with webdriver.Firefox(options=options) as driver:
        driver.get("http://demo.testarena.pl/logowanie")
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(request.param["login"])
        pass_input = driver.find_element(By.ID, "password")
        pass_input.send_keys(request.param["password"])
        driver.find_element(By.ID, "login").click()
        yield driver
        driver.quit()


def find_element_in_menu(driver: webdriver.Firefox, element: str) -> Union[None, bool]:
    menu = driver.find_element(By.CLASS_NAME, "menu")
    elems = menu.find_elements(By.TAG_NAME, "a")
    for item in elems:
        if element in item.text:
            item.click()
            return
    return False


def wait_until_element_is_loaded(
    driver: webdriver.Firefox, timeout: int, locator: str, element: str
) -> bool:
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((locator, element))
        )
        return True
    except PageNotLoaded as e:
        logger.error("Exception occurred: ", e)
        return False
