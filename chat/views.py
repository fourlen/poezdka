from django.http import HttpRequest, JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import chat.db_communication as db_communication
from loguru import logger
import json

@csrf_exempt
def get_chat(request: HttpRequest):
    try:
        logger.debug(request.body)
        values = json.loads(request.body)
        return JsonResponse(db_communication.get_chat_messages(from_id=values['from_id'], to_id=values['to_id']), safe=False)
    except Exception as err:
        logger.exception(err)
        return HttpResponseServerError(f'Something goes wrong: {err}')
