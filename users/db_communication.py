import hashlib

from . import utils
from .models import Users


def get_user(**kwargs) -> Users:
    return Users.objects.filter(
        **kwargs
    ).first()


def delete_user(token: str):
    Users.objects.filter(
        token=token
    ).delete()


def add_user(values: dict) -> str:
    token = utils.calculate_token(values['login'])
    user = Users(
            login=values['login'],
            password=hashlib.sha256(values['password'].encode("utf-8")).hexdigest(),
            token=token,
            firstname=values['firstname'],
            lastname=values['lastname'],
            gender=values['gender'],
            birth=values['birth']
        )
    user.save()
    return token
