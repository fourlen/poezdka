from .models import Message


def get_chat_messages(from_id, to_id):
    return [{
        'from': message.from_user.id,
        'to': message.to_user.id,
        'message': message.message
    } for message in Message.objects.filter(user_from_id=from_id, user_to_id=to_id)]