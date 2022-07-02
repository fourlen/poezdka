from .models import Users
import hashlib
import utils

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


def update_user(values: dict, token: str):
    user = get_user(
        token=token
    )
    user.firstname = values['firstname']
    user.lastname = values['lastname']
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