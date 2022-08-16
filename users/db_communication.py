import base64

from django.core.files.base import ContentFile

from trips.models import Trips
from .models import Users, Review
import hashlib
from users import utils
import cars.db_communication as cars_db
import booking.db_communication as booking_db


def add_user(values: dict, token=None) -> tuple:
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
    return token, user


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
    user.first_name = values['firstname']
    user.last_name = values['lastname']
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
    user = Users.objects.filter(
        **kwargs
    ).first()
    if 'token' in kwargs and not user.is_active:
        raise Exception("Your account has been blocked. Please, contact support")
    return user


def delete_user(token: str) -> None:
    get_user(token=token).delete()


def get_user_as_json(user) -> dict:
    return {
        "id": user.id,
        "token": user.token,
        "login": user.login,
        "photo": get_photo(user),
        "firstname": user.first_name,
        "lastname": user.last_name,
        "gender": user.gender,
        "birth": user.birth,
        "cars": cars_db.get_all_cars_as_json(user.token),
    }


def get_user_for_trip(user: Users, trip=None) -> dict:
    return {
        "id": user.id,
        "photo": get_photo(user),
        "phone": user.login if utils.is_phone_number(user.login) else None,
        "firstname": user.first_name,
        "lastname": user.last_name,
        "seat": booking_db.get_user_seat(user, trip) if trip else "owner"
    }


def change_photo(user: Users, photo: str):
    if photo:
        format, imgstr = photo.split(';base64,')
        ext = format.split('/')[-1]
        data = ContentFile(base64.b64decode(imgstr), name=f'{user.login}_ava.{ext}')
        user.photo = data
    else:
        user.photo = None
    user.save()
    return user.photo


def get_photo(user: Users):
    return user.photo.url if user.photo else None


def set_review(user, id_, message, mark):
    if mark not in [1, 2, 3, 4, 5]:
        raise Exception("Incorrect_mark")
    review = Review(
        owner=user,
        user=get_user(id=id_),
        message=message,
        mark=mark
    )
    review.save()


def get_json_review(review: Review):
    return {
        "from": get_user_for_review(review.owner),
        "message": review.message,
        "mark": review.mark,
        "date": review.date
    }


def get_user_for_review(user: Users) -> dict:
    return {
        "id": user.id,
        "photo": get_photo(user),
        "firstname": user.first_name,
        "lastname": user.last_name,
    }


def get_my_reviews(token):
    all_reviews = Review.objects.filter(user=get_user(token=token)).all()
    return {
        "average": utils.count_average(all_reviews),
        "reviews": list(
            map(
                get_json_review, all_reviews
            )
        )
    }
