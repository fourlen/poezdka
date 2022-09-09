import base64
from django.core.files.base import ContentFile
from .exceptions import NotExistException, NotValidException
from .models import Users, Review, Questions, Blog
import hashlib
from users import utils
import cars.db_communication as cars_db
import booking.db_communication as booking_db


def add_user(values: dict, token=None) -> tuple:
    if not token:
        token = utils.calculate_token(values['login'])
    login = values['login']
    email = login if utils.is_email(login) else None
    phone = login if utils.is_phone_number(login) else None
    user = Users(
        login=login,
        password=hashlib.sha256(values['password'].encode("utf-8")).hexdigest(),
        token=token,
        first_name=values['firstname'],
        last_name=values['lastname'],
        gender=values['gender'],
        birth=values['birth'],
        email=email,
        phone_number=phone,
        fcm_token=values['fcm_token']
    )
    user.save()
    return token, user


def oauth_user(user):
    print(user)
    if user["email"]:
        if get_user(login=user["email"]):
            return get_user_as_json(get_user(login=user["email"]))
        else:
            token = utils.calculate_token(user["email"])
            user = Users(
                login=user["email"],
                token=token,
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user["email"],
                fcm_token=user['fcm_token']
            )
            user.save()
            return get_user_as_json(user)
    elif "phone_number" in user:
        if get_user(login=user["phone_number"]):
            return get_user_as_json(get_user(login=user["email"]))
        else:
            token = utils.calculate_token(user["phone_number"])
            user = Users(
                login=user["phone_number"],
                token=token,
                first_name=user["first_name"],
                last_name=user["last_name"],
                phone_number=user["phone_number"],
            )
            user.save()
            return get_user_as_json(user)


def update_user(values: dict, token: str):
    user = get_user(
        token=token
    )
    if values['first_name']:
        user.first_name = values['first_name']
    if values['last_name']:
        user.last_name = values['last_name']
    if values['gender']:
        user.gender = values['gender']
    if values['birth']:
        user.birth = values['birth']
    if "phone_number" in values:
        if values['phone_number']:
            user.phone_number = values['phone_number']
    if "email" in values:
        if values['email']:
            user.email = values['email']
    user.save()
    return get_user_as_json(user)

def get_user(**kwargs) -> Users:
    user = Users.objects.filter(
        **kwargs
    ).first()
    if user:
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
        "email": user.email,
        "phone_number": user.phone_number,
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
        "seat": booking_db.get_user_seat(user, trip) if trip else "owner",
        "phone_number": user.phone_number,
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
    return get_user_as_json(user)


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


def reset_password1(login):
    if utils.is_email(login):
        user = get_user(email=login)
        if not user:
            raise NotExistException
        if not user.token:
            raise Exception("Oauth account. Please, enter with Gmail, Apple or VK")
        code = utils.send_mail_reset(login)
        if code:
            user.code = code
            user.save()
            return {
                "type": "email",
                "login": login
            }
    elif utils.is_phone_number(login):
        user = get_user(phone_number=login)
        if not user:
            raise NotExistException
        code = utils.send_phone_reset(login)
        if code:
            user.code = code
            user.save()
        return {
            "type": "phone",
            "login": login
        }
    else:
        raise NotValidException("login must be email or phone number")


def check_code(code, login):
    if utils.is_email(login):
        user = get_user(email=login)
        if not user:
            raise NotExistException
    elif utils.is_phone_number(login):
        user = get_user(phone_number=login)
        if not user:
            raise NotExistException
    else:
        raise Exception("login must be email or phone number")
    if not user.code:
        raise Exception("No need a code")
    if user.code == code:
        user.code = 0
        user.save()
        return {
            "is_correct": True,
            "token": user.token
        }
    else:
        return {
            "is_correct": False
        }


def reset_password2(token, password):
    user = get_user(token=token)
    if not user:
        raise NotExistException
    user.password = hashlib.sha256(password.encode("utf-8")).hexdigest()
    user.save()


def get_questions():
    return {
        "questions":
            [
                {
                    "question": i.question,
                    "answer": i.answer
                }
                for i in Questions.objects.all()
            ]
        }


def get_blog():
    return {
        "blog":
            [
                {
                    "image": i.image.url if i.image else None,
                    "header": i.header,
                    "text": i.text
                }
                for i in Blog.objects.all()
            ]
        }
