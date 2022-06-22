from django.shortcuts import render
from django.http import HttpRequest, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from users.models import Users
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

@csrf_exempt
def registration(request: HttpRequest):
    try:
        values = json.loads(request.body)
        if values['gender'] != 'male' and values['gender'] != 'female':
            return HttpResponseBadRequest("gender must be male or female")
        if not (re.match(r'^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$', values['login']) or re.match(r'^(\+7|7|8)?[\s\-]?\(?[489][0-9]{2}\)?[\s\-]?[0-9]{3}[\s\-]?[0-9]{2}[\s\-]?[0-9]{2}', values['login'])):
            return HttpResponseBadRequest("login must be email or phone number")
        token = jwt.encode({
            'login': values['login'],
            'timestamp': str(time())
        }, key=SECRET_KEY)
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