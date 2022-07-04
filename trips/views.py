import json

from django.http import HttpRequest, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import trips.db_communication as db


@csrf_exempt
def add_trip(request: HttpRequest):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        token = request.headers.get('Authorization')
        return JsonResponse(
            db.add_trip(values, token)
        )
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


