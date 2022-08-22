import json
import re
import random

import jwt
import requests
from django.core.mail import send_mail

from poezdka.settings import SECRET_KEY, EMAIL_HOST_USER
from time import time


def check_gender(gender: str) -> bool:
    return gender == 'male' or gender == 'female'


def is_email(string: str):
    return re.fullmatch(r'[^@]+@[^@]+\.[^@]+', string)


def is_phone_number(string: str):
    return re.fullmatch(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}', string)


def calculate_token(login: str):
    return jwt.encode({
        'login': login,
        'timestamp': str(time())
    }, key=SECRET_KEY)


def count_average(reviews):
    sum_ = 0
    for i in reviews:
        sum_ += i.mark
    return sum_ / len(reviews) if len(reviews) != 0 else 0


def send_mail_reset(email):
    code = random.randint(100000, 999999)
    if send_mail('Your code',
                     f'Введите этот код для подтвержения личности на сервисе Poezdka:'
                     f' {code}',
                     EMAIL_HOST_USER,
                     [email],
                     fail_silently=False, ):
        return code
    else:
        return 0


def send_phone_reset(phone):
    code = random.randint(100000, 999999)
    body = json.dumps(
        {
            "messages": [
                {
                    "phone": phone,
                    "sender": "SMS DUCKOHT",
                    "clientId": "1",
                    "text": "Ваш код для восстановления пароля: " + str(code) + ". Никому не говорите код!"
                }
            ],
            "statusQueueName": "myQueue",
            "showBillingDetails": True,
            "login": "z1661155504531",
            "password": "656792"
        }
    )
    r = requests.post('https://api.iqsms.ru/messages/v2/send.json', data=body)
    print(r.text)
    return code
