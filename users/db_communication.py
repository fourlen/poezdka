from .models import Users
import hashlib
from users import utils
import cars.db_communication as cars_db


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
        birth=values['birth'],
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
    return {
        "token": token,
        "login": user.login,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "gender": None,
        "birth": None,
        "cars": None,
    }


def update_user(values: dict, token: str):
    user = get_user(
        token=token
    )
    user.firstname = values['firstname']
    user.lastname = values['lastname']
    user.gender = values['gender']
    user.birth = values['birth']
    user.save()
    return {
            "login": user.login,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "gender": user.gender,
            "birth": user.birth,
            "cars": cars_db.get_all_cars_as_json(token)
        }


def get_user(**kwargs) -> Users:
    return Users.objects.filter(
        **kwargs
    ).first()


def delete_user(token: str) -> None:
    get_user(token=token).delete()


def get_user_as_json(user) -> dict:
    return {
        "token": user.token,
        "login": user.login,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "gender": user.gender,
        "birth": user.birth,
        "cars": cars_db.get_all_cars_as_json(user.token),
    }


def get_user_for_trip(user) -> dict:
    return {
        "phone": user.login if utils.is_phone_number(user.login) else None,
        "firstname": user.first_name,
        "lastname": user.last_name,
    }
