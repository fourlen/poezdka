import re
import jwt
from poezdka.settings import SECRET_KEY
from time import time


def check_gender(gender: str) -> bool:
    return gender == 'male' or gender == 'female'


def is_email(string: str):
    return re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', string)


def is_phone_number(string: str):
    return re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}', string)


def calculate_token(login: str) -> str:
    return jwt.encode({
            'login': login,
            'timestamp': str(time())
        }, key=SECRET_KEY)