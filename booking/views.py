from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponseServerError, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import booking.db_communication as db
from booking.exceptions import *
from booking.exceptions import *


@csrf_exempt
def book(request: HttpRequest, id_: int):
    try:
        if request.method != 'POST':
            return HttpResponseBadRequest("Wrong request method (GET, POST, PUT, DELETE)")
        token = request.headers.get('Authorization')
        return JsonResponse(
            {"success": True,
             "status": "You are successfully book",
             "booking_id": db.book(token, id_)}
        )
    except AlreadyInTripException:
        return HttpResponseServerError('You are already in trip')
    except IntegrityError:
        return HttpResponseServerError('You are not authorized')
    except NotExistException:
        return HttpResponseServerError('Trip does not exist')
    except BannedUserException:
        return HttpResponseServerError('You were cancel this trip yet')
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')


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
        return HttpResponseServerError('Booking does not exist')
    except Exception as ex:
        return HttpResponseServerError(f'Something goes wrong: {ex}')
