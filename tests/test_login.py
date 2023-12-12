from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from faker import Faker

from resources.logger import get_logger
from resources.utils import extract_data, get_unique_string
from resources.browser import driver, logged_in_driver
from resources.exceptions import PageNotLoaded

import pytest
import time
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
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "email"))
        )
    except PageNotLoaded as e:
        logger.error("Exception occurred: ", e)

    logger.info(driver.current_url)
    email_input = driver.find_element(By.ID, "email")
    email_input.send_keys(login)
    pass_input = driver.find_element(By.ID, "password")
    pass_input.send_keys(password)
    driver.find_element(By.ID, "login").click()
    
    logger.info(driver.current_url)


@pytest.mark.parametrize(
        "logged_in_driver",[{"login": "administrator@testarena.pl", "password": "sumXQQ72$L"}], indirect=True)
def test_create_new_directory(logged_in_driver):
    driver = logged_in_driver

    logger = get_logger(__name__)

    fake = Faker()
    dir_name = fake.name().replace(' ', '_')
    menu = driver.find_element(By.CLASS_NAME, "menu")
    elems = menu.find_elements(By.TAG_NAME, "a")
    for item in elems:
        if "Projekt" in item.text:
            # item.get_attribute('href')
            item.click()
            break

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "collapse"))
        )
    except PageNotLoaded as e:
        logger.error("Exception occurred: ", e)

    buttons = driver.find_element(By.CLASS_NAME, "button_link_ul")
    attachement = buttons.find_elements(By.TAG_NAME, "li")
    attachement[1].click()
    attachement[1].find_elements(By.TAG_NAME, "li")[0].click()
    
    driver.switch_to.window(driver.window_handles[1])

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "iconDirectory"))
        )
    except PageNotLoaded as e:
        logger.error("Exception occurred: ", e)

    driver.find_element(By.ID, "createDirectoryButton").click()

    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "directoryName"))
        )
    except PageNotLoaded as e:
        logger.error("Exception occurred: ", e)

    driver.find_element(By.ID, "directoryName").send_keys(dir_name)
    driver.find_element(By.ID, "createDirectoryPopupButton").click()
    
    list_of_files = driver.find_element(By.TAG_NAME, "tbody")
    files = list_of_files.find_elements(By.TAG_NAME, "tr")
    for file in files:
        logger.warning(file.text)
    
    assert any(dir_name in file.text for file in files), "File not created successfuly"


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
