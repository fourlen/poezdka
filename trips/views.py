import json

from django.http import HttpRequest, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import trips.db_communication as db
from trips.models import Trips
from users.models import Users


@csrf_exempt
def add_trip(request: HttpRequest):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        values = json.loads(request.body)
        token = request.headers.get('Authorization')
        db.add_trip(values, token)
        return JsonResponse({
            "success": True,
            "status": "Trip created"
        })
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


@csrf_exempt
def get_trips(request: HttpRequest):
    try:
        if request.method != 'GET':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        return JsonResponse({
            "trips": db.get_trips_as_json(token)
        })
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')
