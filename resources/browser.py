from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
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

