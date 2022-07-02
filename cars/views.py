import json

from django.db import IntegrityError
from django.http import HttpRequest, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from cars import db_communication as db


@csrf_exempt
def add_car(request: HttpRequest):
    try:
        values = json.loads(request.body)
        token = request.headers.get('Authorization')
        db.add_car(token, mark=values["mark"], model=values["model"], color=values["color"],
                         vehicle_number=values["vehicle_number"], count_of_passengers=values["count_of_passengers"])
        return JsonResponse(
            {
                "success": True,
            }
        )
    except IntegrityError as ex:
        return HttpResponseBadRequest("Car already exist")
    except Exception as ex:
        return HttpResponseBadRequest(ex)


@csrf_exempt
def delete_car(request: HttpRequest, id_: int):
    try:
        token = request.headers.get('Authorization')
        status = db.delete_car(token, id_)
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
                    "success": True
                }
            )
    except Exception as ex:
        return HttpResponseBadRequest(ex)
