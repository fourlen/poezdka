from .models import Users
import hashlib
from users import utils


def add_user(values: dict, token=None) -> str:
    if not token:
        token = utils.calculate_token(values['login'])
    user = Users(
        login=values['login'],
        password=hashlib.sha256(values['password'].encode("utf-8")).hexdigest(),
        token=token,
        first_name=values['firstname'],
        last_name=values['lastname'],
        gender=values['gender'],
        birth=values['birth']
    )
    user.save()
    return token


def add_oauth_user(values: dict):
    token = utils.calculate_token(values['login'])
    user = Users(
        login=values['login'],
        token=token,
        first_name=values['first_name'],
        last_name=values['last_name'],
    )
    user.save()


def update_user(values: dict, token: str):
    user = get_user(
        token=token
    )
    user.firstname = values['first_name']
    user.lastname = values['last_name']
    user.gender = values['gender']
    user.birth = values['birth']
    user.save()


def get_user(**kwargs) -> Users:
    return Users.objects.filter(
        **kwargs
    ).first()


def delete_user(token: str):
    Users.objects.filter(
        token=token
    ).delete()
