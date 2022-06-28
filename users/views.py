from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import re
import jwt
from time import time
from poezdka.settings import SECRET_KEY
import hashlib
import json
import users.db_communication as db


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
from users import utils
from users.models import Users


@csrf_exempt
def registration(request: HttpRequest):
    try:
        values = json.loads(request.body)
        if values['gender'] != 'male' and values['gender'] != 'female':
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
        return HttpResponseBadRequest(f'Something goes wrong: {err}')


# request:
# {
#     "token": str
# }
# response
# {
#     success: bool,
#     error: if not success
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
        return JsonResponse({
            'success': False,
            'error': err
        })
