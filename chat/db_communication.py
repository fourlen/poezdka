from .models import Message


def get_chat_messages(from_id, to_id):
    return [{
        'time': message.time,
        'from': message.from_user.id,
        'to': message.to_user.id,
        'message': message.text
    } for message in sorted(list(Message.objects.filter(from_user_id=from_id, to_user_id=to_id)) + list(
        Message.objects.filter(from_user_id=to_id, to_user_id=from_id)),
                            key=lambda x: x.time)]
