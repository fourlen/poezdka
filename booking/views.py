import json

from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import booking.db_communication as db
from booking.exceptions import *


@csrf_exempt
def book(request: HttpRequest, id_: int):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        values = json.loads(request.body)
        return JsonResponse(
            {"success": True,
             "status": "You are successfully book",
             "booking_id": db.book(token, id_, values["seats"] if "seats" in values else None)}
        )
    except IntegrityError:
        return HttpResponseBadRequest('You are not authorized')
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')


@csrf_exempt
def cancel_booking(request: HttpRequest, id_: int):
    try:
        if request.method != 'DELETE':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        status = db.cancel_booking(token, id_)
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
    except NotExistException:
        return HttpResponseBadRequest('Booking does not exist')
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')


@csrf_exempt
def cancel_booking_for_driver(request: HttpRequest):
    try:
        if request.method != 'DELETE':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        values = json.loads(request.body)
        status = db.cancel_booking_for_driver(token, values['trip_id'], values['user_id'])
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
    except NotExistException:
        return HttpResponseBadRequest('Booking does not exist')
    except Exception as ex:
        return HttpResponseBadRequest(f'Something goes wrong: {ex}')
