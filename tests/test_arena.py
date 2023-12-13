from selenium import webdriver
from selenium.webdriver.common.by import By

from faker import Faker

from resources.browser import (
    logged_in_driver,
    insert_data_to_form,
    wait_until_element_is_loaded,
    find_element_in_menu,
)

import pytest


@pytest.mark.parametrize(
    "logged_in_driver",
    [{"login": "administrator@testarena.pl", "password": "sumXQQ72$L"}],
    indirect=True,
)
def test_create_new_task(logged_in_driver):
    driver = logged_in_driver
    fake = Faker()

    # goto 'Zadania'
    find_element_in_menu(driver, "Zadania")

    # create new task
    wait_until_element_is_loaded(driver, 10, By.CLASS_NAME, "filterBox")
    driver.find_element(By.CLASS_NAME, "button_link").click()
    wait_until_element_is_loaded(driver, 10, By.ID, "title")

    # insert data to form
    driver.find_element(By.ID, "title").send_keys(fake.name())
    driver.find_element(By.ID, "description").send_keys(fake.sentence())
    insert_data_to_form(driver, By.ID, "token-input-environments", "Safari")
    insert_data_to_form(driver, By.ID, "token-input-versions", "mojaWersja")
    insert_data_to_form(driver, By.ID, "dueDate", "2022-08-09 23:59")
    driver.find_element(By.ID, "j_assignToMe").click()
    driver.find_element(By.ID, "save").click()

    # verify task created
    wait_until_element_is_loaded(driver, 100, By.ID, "j_info_box")


@pytest.mark.parametrize(
    "logged_in_driver",
    [{"login": "administrator@testarena.pl", "password": "sumXQQ72$L"}],
    indirect=True,
)
def test_create_new_directory(logged_in_driver):
    driver = logged_in_driver
    fake = Faker()
    dir_name = fake.name().replace(" ", "_")

    # goto "Projekt"
    find_element_in_menu(driver, "Projekt")

    # goto add new plan
    buttons = driver.find_element(By.CLASS_NAME, "button_link_ul")
    attachement = buttons.find_elements(By.TAG_NAME, "li")
    attachement[1].click()
    attachement[1].find_elements(By.TAG_NAME, "li")[0].click()

    # switch to new window and wait until loaded
    driver.switch_to.window(driver.window_handles[1])
    wait_until_element_is_loaded(driver, 10, By.CLASS_NAME, "iconDirectory")

    # find create new directory button
    driver.find_element(By.ID, "createDirectoryButton").click()
    wait_until_element_is_loaded(driver, 10, By.ID, "directoryName")

    # insert name of directory and create
    driver.find_element(By.ID, "directoryName").send_keys(dir_name)
    driver.find_element(By.ID, "createDirectoryPopupButton").click()

    # wait until dir is created and verify
    list_of_files = wait_until_element_is_loaded(driver, 2, By.TAG_NAME, "tbody")
    list_of_files = driver.find_element(By.TAG_NAME, "tbody")
    files = list_of_files.find_elements(By.TAG_NAME, "tr")
    assert any(dir_name in file.text for file in files), "File not created successfuly"
