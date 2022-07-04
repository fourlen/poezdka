from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest, \
    HttpResponseServerError, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json
import users.db_communication as db
import cars.db_communication as cars_db
from users import utils


# request
# {
#     "login": str,
#     "password"" str,
#     "firstname": str,
#     "lastname": str,
#     "gender": str ("male" or "female"),
#     "birth": int (timestamp)
# }
# response
# {
#     "token": token
# }
from users.models import Users


@csrf_exempt
def registration(request: HttpRequest):
    try:
        values = json.loads(request.body)
        if utils.check_gender(values['gender']):
            return HttpResponseBadRequest("gender must be male or female")
        if not (utils.is_phone_number(values['login']) or utils.is_email(values['login'])):
            return HttpResponseBadRequest("login must be email or phone number")
        token = db.add_user(values)
        return JsonResponse({
            "token": token
        })
    except Exception as err:
        return HttpResponseBadRequest(f"Somethong goes wrong: {err}")


# request
# {
#     'login': str,
#     'password': str
# }
# reponse:
# {
#     'authorized': bool,
#     'token': str (if authorized)
#     'error': str (if not authorized)
# }

@csrf_exempt
def auth(request: HttpRequest):
    print(request.headers)
    try:
        values = json.loads(request.body)
        login = values['login']
        password = hashlib.sha256(values['password'].encode("utf-8")).hexdigest()
        user = db.get_user(
            login=login
        )
        if user is None:
            return JsonResponse({
                'authorized': True,
                'error': 'User with such login does not exists'
            })
        if user.password == password:
            return JsonResponse({
                'authorized': True,
                'token': user.token
            })
        return JsonResponse({
            'authorized': False,
            'error': 'Wrong password'
        })
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')


# request:
# {
#     "token": str
# }
# response
# {
#     success: True if success else Server error
# }

@csrf_exempt
def delete_user(request: HttpRequest):
    try:
        token = request.headers.get('Authorization')
        db.delete_user(
            token=token
        )
        return JsonResponse({
            'success': True
        })
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')


@csrf_exempt
def get_user(request: HttpRequest):
    try:
        token = request.headers.get('Authorization')
        user = db.get_user(
            token=token
        )
        if not user:
            user = request.user
            db.add_oauth_user({
                "login": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            })
            return JsonResponse({
                "login": user.email,
                "firstname": user.first_name,
                "lastname": user.last_name,
                "gender": None,
                "birth": None,
                "cars": None,
            })
        return JsonResponse({
            "login": user.login,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "gender": user.gender,
            "birth": user.birth,
            "cars": cars_db.get_all_cars_as_json(
                owner=user
            )
        })
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')


def update_user(request: HttpRequest):
    try:
        token = request.headers.get('Authorization')
        values = json.loads(request.body)
        if not utils.check_gender(values['gender']):
            return HttpResponseBadRequest("gender must be male or female")
        if not values['birth'].isdigit():
            return HttpResponseBadRequest("birth must be integer")
        db.update_user(values, token)
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')
