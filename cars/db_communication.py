from cars.models import Auto
import users.db_communication as users_db
from django.core import serializers
import json


def add_car(values, token: str):
    car = Auto(
        owner=users_db.get_user(token=token),
        mark=values["mark"],
        model=values["model"],
        color=values["color"],
        vehicle_number=values["vehicle_number"],
        count_of_passengers=values["count_of_passengers"],
    )
    car.save()


def delete_car(token: str, id_: int):
    user = users_db.get_user(token=token)
    car = Auto.objects.get(id=id_)
    flag = car.owner == user
    if flag:
        car.delete()
    return flag


def get_car(id_: int):
    return Auto.objects.get(id=id_)


def get_all_cars(token):
    user = users_db.get_user(token=token)
    return Auto.objects.filter(owner=user).all()


def get_all_cars_as_json(token):
    return [{
            'pk': car.id,
            'owner': car.owner.id,
            'mark': car.mark,
            'model': car.model,
            'color': car.color,
            'vehicle_number': car.vehicle_number,
            'count_of_passengers': car.count_of_passengers
        } for car in get_all_cars(token)]
    # return json.loads(serializers.serialize("json", get_all_cars(token)))
