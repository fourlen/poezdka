from cars.models import Auto
import users.db_communication as users_db
from django.core import serializers
import json


def add_car(token: str, mark=None, model=None, color=None,
            vehicle_number=None, count_of_passengers=None):
    car = Auto(owner=users_db.get_user(token=token), mark=mark, model=model, color=color,
               vehicle_number=vehicle_number, count_of_passengers=count_of_passengers)
    car.save()


def delete_car(token: str, id_: int):
    user = users_db.get_user(token=token)
    car = Auto.objects.get(id=id_)
    flag = car.owner is user
    if flag:
        car.delete()
    return flag


def get_all_cars(**kwargs):
    return Auto.objects.filter(**kwargs).all()


def get_all_cars_as_json(**kwargs):
    return json.loads(serializers.serialize("json", Auto.objects.filter(**kwargs).all()))
