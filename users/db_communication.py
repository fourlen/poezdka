from .models import Users

def get_user(**kwargs) -> Users:
    return Users.objects.filter(
        **kwargs
    ).first()


def delete_user(token: str):
    Users.objects.filter(
        token=token
    ).delete()