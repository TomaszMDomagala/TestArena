from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import get_logger
from exceptions import IncorectLoginData, PageNotLoaded

import re
import time

logger = get_logger(__name__)

    
def extract_data(data: str) -> tuple[str, str]:
    login = re.findall(r"Login: (.+)", data)
    password = re.findall(r"Haslo|Hasło: (.+)", data)
    if len(login) != 1 or len(password) != 1:
        raise IncorectLoginData(login, password)
    return (login[0], password[0])


driver = webdriver.Firefox()
driver.get("http://testarena.pl/demo")

# logger.warning(driver.current_url)
print(driver.window_handles)
print(driver.current_window_handle)

description = driver.find_element(By.CLASS_NAME, "description")
items = description.find_elements(By.TAG_NAME, 'p')
login, password = extract_data(items[0].text)
demo_button = items[1].find_element(By.TAG_NAME, 'a')

demo_button.click()
print(driver.window_handles)
# driver.close()

login_page = driver.switch_to.window(driver.window_handles[1])
print(driver.window_handles)
print(driver.current_window_handle)
# try:
#     element = WebDriverWait(driver, 200, 5).until(EC.presence_of_element_located((By.TAG_NAME, "form")))
# finally:
#     raise PageNotLoaded()
time.sleep(2)
print(driver.current_url)

email_input = driver.find_element(By.ID, "email")
email_input.send_keys(login)
pass_input = driver.find_element(By.ID, "password")
pass_input.send_keys(password)
driver.find_element(By.ID, "login").click()

print(driver.window_handles)

# time.sleep(10)
# logger.warning(login_page.current_url)
# logger.warning(demo_button.get_attribute('href'))

# driver.close()
# driver.quit()
