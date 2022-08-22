from django.contrib.auth import logout
from django.http import HttpRequest, HttpResponseNotFound, JsonResponse, HttpResponseBadRequest, \
    HttpResponseServerError, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import json

from loguru import logger
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
from users.exceptions import *
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
        token, user = db.add_user(values)
        return JsonResponse({
            "token": token,
            "id": user.id,
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
                'token': user.token,
                "id": user.id,
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
        return JsonResponse(
            db.get_user_as_json(
                db.get_user(
                    token=token
                )
            )
        )
    except Exception as err:
        logger.error(err)
        return HttpResponseServerError(f'Something goes wrong: {err}')


@csrf_exempt
def oauth_user(request: HttpRequest):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        return JsonResponse(
            db.oauth_user(json.loads(request.body))
        )
    except Exception as err:
        logger.error(err)
        return HttpResponseServerError(f'Something goes wrong: {err}')


@csrf_exempt
def update_user(request: HttpRequest):
    try:
        if request.method != 'PUT':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        values = json.loads(request.body)
        if values['gender'] and not utils.check_gender(values['gender']):
            return HttpResponseBadRequest("gender must be male or female")
        return JsonResponse(
            db.update_user(values, token)
        )
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')


@csrf_exempt
def change_photo(request: HttpRequest):
    try:
        if request.method != 'PUT':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        user = db.get_user(token=token)
        values = json.loads(request.body)
        return JsonResponse(
            db.change_photo(user, values["photo"])
        )
    except Exception as ex:
        return HttpResponseBadRequest(ex)


@csrf_exempt
@api_view(['POST'])
def review(request: HttpRequest, id_: int) -> HttpResponse:
    try:
        token = request.headers.get('Authorization')
        user = db.get_user(token=token)
        values = json.loads(request.body)
        db.set_review(user, id_, values["message"], values["mark"])
        return JsonResponse(
            {
                "status": "The review was successfully left"
            }
        )
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


@csrf_exempt
@api_view(['GET'])
def get_reviews(request: HttpRequest) -> HttpResponse:
    try:
        token = request.headers.get('Authorization')
        return JsonResponse(db.get_my_reviews(token))
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


@csrf_exempt
@api_view(['POST'])
def reset_password(request: HttpRequest) -> HttpResponse:
    try:
        values = json.loads(request.body)
        return JsonResponse(db.reset_password1(values["login"]))
    except NotExistException:
        return HttpResponseBadRequest('Can\'t find user')
    except NotValidException as ex:
        return HttpResponseBadRequest(ex)
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


@csrf_exempt
@api_view(['POST'])
def check_code(request: HttpRequest) -> HttpResponse:
    try:
        values = json.loads(request.body)
        return JsonResponse(db.check_code(values["code"], values["email"]))
    except NotExistException:
        return HttpResponseBadRequest('Can\'t find user')
    except NotValidException as ex:
        return HttpResponseBadRequest(ex)
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


@csrf_exempt
@api_view(['POST'])
def reset_password_confirm(request: HttpRequest) -> HttpResponse:
    try:
        token = request.headers.get('Authorization')
        values = json.loads(request.body)
        db.reset_password2(token, values["password"])
        return Response(status=status.HTTP_204_NO_CONTENT)
    except NotExistException:
        return HttpResponseBadRequest('Can\'t find user')
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


@csrf_exempt
@api_view(['GET'])
def get_questions(request: HttpRequest) -> HttpResponse:
    try:
        return JsonResponse(
            db.get_questions()
        )
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


@csrf_exempt
@api_view(['GET'])
def get_blog(request: HttpRequest) -> HttpResponse:
    try:
        return JsonResponse(
            db.get_blog()
        )
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')
