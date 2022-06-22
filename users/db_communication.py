from .models import Users

def get_user(**kwargs) -> Users:
    return Users.objects.filter(
        **kwargs
    ).first()