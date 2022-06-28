import re
import jwt
from poezdka.settings import SECRET_KEY
import time

def is_phone_number(string: str) -> bool:
    return re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', string)


def is_email(string: str) -> bool:
    return re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}', string)


def calculate_token(login: str) -> str:
    return jwt.encode({
            'login': login,
            'timestamp': str(time())
        }, key=SECRET_KEY)