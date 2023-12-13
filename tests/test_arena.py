from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from faker import Faker

from resources.logger import get_logger
from resources.browser import (
    logged_in_driver,
    wait_until_element_is_loaded,
    find_element_in_menu,
)
from resources.exceptions import PageNotLoaded

import pytest
import time


@pytest.mark.parametrize(
    "logged_in_driver",
    [{"login": "administrator@testarena.pl", "password": "sumXQQ72$L"}],
    indirect=True,
)
def test_create_new_task(logged_in_driver):
    driver = logged_in_driver

    logger = get_logger(__name__)
    fake = Faker()

    find_element_in_menu(driver, "Zadania")

    wait_until_element_is_loaded(driver, 10, By.CLASS_NAME, "filterBox")

    driver.find_element(By.CLASS_NAME, "button_link").click()

    wait_until_element_is_loaded(driver, 10, By.ID, "title")

    logger.info("updating form")
    driver.find_element(By.ID, "title").send_keys(fake.name())
    driver.find_element(By.ID, "description").send_keys(fake.sentence())

    driver.find_element(By.ID, "token-input-environments").click()
    driver.find_element(By.ID, "token-input-environments").send_keys("Safari")
    time.sleep(0.5)
    driver.find_element(By.ID, "token-input-environments").send_keys(Keys.RETURN)

    driver.find_element(By.ID, "token-input-versions").click()
    driver.find_element(By.ID, "token-input-versions").send_keys("mojaWersja")
    time.sleep(0.5)
    driver.find_element(By.ID, "token-input-versions").send_keys(Keys.RETURN)

    driver.find_element(By.ID, "dueDate").click()
    driver.find_element(By.ID, "dueDate").send_keys("2022-08-09 23:59")
    driver.find_element(By.ID, "dueDate").send_keys(Keys.RETURN)

    driver.find_element(By.ID, "j_assignToMe").click()
    driver.find_element(By.ID, "save").click()

    logger.info("verify form")
    wait_until_element_is_loaded(driver, 100, By.ID, "j_info_box")


@pytest.mark.parametrize(
    "logged_in_driver",
    [{"login": "administrator@testarena.pl", "password": "sumXQQ72$L"}],
    indirect=True,
)
def test_create_new_directory(logged_in_driver):
    driver = logged_in_driver

    logger = get_logger(__name__)

    fake = Faker()
    dir_name = fake.name().replace(" ", "_")

    find_element_in_menu(driver, "Projekt")

    wait_until_element_is_loaded(driver, 10, By.CLASS_NAME, "collapse")

    logger.info("go to create directory")
    buttons = driver.find_element(By.CLASS_NAME, "button_link_ul")
    attachement = buttons.find_elements(By.TAG_NAME, "li")
    attachement[1].click()
    attachement[1].find_elements(By.TAG_NAME, "li")[0].click()

    driver.switch_to.window(driver.window_handles[1])

    wait_until_element_is_loaded(driver, 10, By.CLASS_NAME, "iconDirectory")

    driver.find_element(By.ID, "createDirectoryButton").click()

    wait_until_element_is_loaded(driver, 10, By.ID, "directoryName")

    logger.info("creating directory")
    driver.find_element(By.ID, "directoryName").send_keys(dir_name)
    driver.find_element(By.ID, "createDirectoryPopupButton").click()

    list_of_files = wait_until_element_is_loaded(driver, 2, By.TAG_NAME, "tbody")
    list_of_files = driver.find_element(By.TAG_NAME, "tbody")
    files = list_of_files.find_elements(By.TAG_NAME, "tr")

    logger.info("verifying if dir is created")
    assert any(dir_name in file.text for file in files), "File not created successfuly"
