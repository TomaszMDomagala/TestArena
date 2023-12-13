from selenium import webdriver
from selenium.webdriver.common.by import By

from resources.logger import get_logger
from resources.utils import extract_data
from resources.browser import driver, wait_until_element_is_loaded

import pytest
import json


@pytest.mark.parametrize("driver", ["http://testarena.pl/demo"], indirect=True)
def test_login(driver):
    logger = get_logger(__name__)

    logger.info(driver.current_url)
    description = driver.find_element(By.CLASS_NAME, "description")
    items = description.find_elements(By.TAG_NAME, 'p')
    login, password = extract_data(items[0].text)
    logger.info(f"Login: {login}, Passowrd: {password}")

    demo_button = items[1].find_element(By.TAG_NAME, 'a')
    demo_button.click()

    driver.switch_to.window(driver.window_handles[1])
    wait_until_element_is_loaded(driver, 10, By.ID, "email")

    logger.info(driver.current_url)
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(login)
    pass_input = driver.find_element(By.ID, "password")
    pass_input.send_keys(password)
    driver.find_element(By.ID, "login").click()
    
    logger.info(driver.current_url)


@pytest.mark.parametrize("driver", ["http://demo.testarena.pl/logowanie"], indirect=True)
def test_login_incorrect_data(driver):
    logger = get_logger(__name__)

    incorrect_logins_count = 0
    possible_urls = ["http://demo.testarena.pl/logowanie", "http://demo.testarena.pl/zaloguj"]

    with open("tests/data/fake_login_data.json", "r") as login_data:
        logins = json.load(login_data)
        
    for item in logins:
        logger.info(driver.current_url)
        email_input = driver.find_element(By.ID, "email")
        email_input.send_keys(logins[item]["login"])
        pass_input = driver.find_element(By.ID, "password")
        pass_input.send_keys(logins[item]["password"])

        driver.find_element(By.ID, "login").click()
        flags = driver.find_elements(By.CLASS_NAME, "login_form_error")
        if len(flags) > 0:
            incorrect_logins_count += 1
        
        assert driver.current_url in possible_urls, "URL has changed unexpectedly"

    assert incorrect_logins_count == len(logins), "Not all tries were successful"
