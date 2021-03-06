from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest, \
    HttpResponseServerError, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json

from loguru import logger

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
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        if not utils.check_gender(values['gender']):
            return HttpResponseBadRequest("gender must be male or female")
        if not (utils.is_phone_number(values['login']) or utils.is_email(values['login'])):
            return HttpResponseBadRequest("login must be email or phone number")
        token = db.add_user(values)
        return JsonResponse({
            "token": token
        })
    except Exception as err:
        return HttpResponseBadRequest(f"Something goes wrong: {err}")


# request
# {
#     'login': str,
#     'password': str
# }
# response:
# {
#     'authorized': bool,
#     'token': str (if authorized)
#     'error': str (if not authorized)
# }

@csrf_exempt
def auth(request: HttpRequest):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        login = values['login']
        password = hashlib.sha256(values['password'].encode("utf-8")).hexdigest()
        user = db.get_user(
            login=login
        )
        if user is None:
            return JsonResponse({
                'authorized': False,
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
        if request.method != 'DELETE':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
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
        if request.method != 'GET':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        user = db.get_user(
            token=token
        )
        if not user:
            user = request.user
            if not db.get_user(
                    login=user.email,
            ):
                if user.email:
                    return JsonResponse(
                        db.add_oauth_user(
                            {
                                "login": user.email,
                                "first_name": user.first_name,
                                "last_name": user.last_name,
                            }
                        )
                    )
                else:
                    return HttpResponseServerError(f'Something goes wrong: Unauthorized')
            user = db.get_user(
                login=user.email
            )
        return JsonResponse(
            db.get_user_as_json(user)
        )
    except Exception as err:
        logger.error(err)
        return HttpResponseServerError(f'Something goes wrong: Unauthorized')


@csrf_exempt
def update_user(request: HttpRequest):
    try:
        if request.method != 'PUT':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        values = json.loads(request.body)
        if not utils.check_gender(values['gender']):
            return HttpResponseBadRequest("gender must be male or female")
        if not values['birth'].isdigit():
            return HttpResponseBadRequest("birth must be integer")
        return JsonResponse(
            db.update_user(values, token)
        )
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')
