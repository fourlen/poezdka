from django.http import HttpRequest, JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
import chat.db_communication as db_communication
from loguru import logger


@csrf_exempt
def get_chat(request: HttpRequest):
    try:
        return JsonResponse(db_communication.get_chat_messages(from_id=request['from_id'], to_id=request['to_id']))
    except Exception as err:
        logger.exception(err)
        return HttpResponseServerError(f'Something goes wrong: {err}')
