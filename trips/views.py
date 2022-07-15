import json

from django.http import HttpRequest, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import trips.db_communication as db


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
def delete_trip(request: HttpRequest, id_: int):
    try:
        if request.method != 'DELETE':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        status = db.delete_trip(token, id_)
        if not status:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Access denied"
                }
            )
        else:
            return JsonResponse(
                {
                    "success": True,
                    "status": "Trip deleted",
                }
            )
    except Exception as ex:
        return HttpResponseBadRequest(ex)


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


@csrf_exempt
def get_past_trips(request: HttpRequest):
    try:
        if request.method != 'GET':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        return JsonResponse({
            "trips": db.get_past_trips_as_json(token)
        })
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')


@csrf_exempt
def get_booked_trips(request: HttpRequest):
    try:
        if request.method != 'GET':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        return JsonResponse({
            "trips": db.get_booked_trips_as_json(token)
        })
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')


@csrf_exempt
def get_past_booked_trips(request: HttpRequest):
    try:
        if request.method != 'GET':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        return JsonResponse({
            "trips": db.get_past_booked_trips_as_json(token)
        })
    except Exception as err:
        return HttpResponseServerError(f'Something goes wrong: {err}')
