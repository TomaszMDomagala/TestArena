from resources.exceptions import IncorectLoginData
import re

def extract_data(data: str) -> tuple[str, str]:
    login = re.findall(r"Login: (.+)", data)
    password = re.findall(r"Haslo|Hasło: (.+)", data)
    if len(login) != 1 or len(password) != 1:
        raise IncorectLoginData(login, password)
    return (login[0], password[0])