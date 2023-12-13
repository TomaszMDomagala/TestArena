from resources.logger import get_logger

logger = get_logger(__name__)


class IncorectLoginData(Exception):
    def __init__(self, login: list, password: list):
        self.login = login
        self.password = password
        self.log_error()

    def log_error(self):
        if len(self.login) != 1:
            logger.error(f"{self.login}")
            logger.error("Login should contain only one element")
        if len(self.password) != 1:
            logger.error(f"{self.password}")
            logger.error("Password should contain only one element")


class PageNotLoaded(Exception):
    def __init__(self):
        logger.error("Page was not loaded properly")
