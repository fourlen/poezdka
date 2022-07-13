from trips.models import Trips
from django.core import serializers
import json
import users.db_communication as users_db
import cars.db_communication as cars_db


def get_all_trips(**kwargs):
    Trips.objects.filter(**kwargs).all()


def get_all_trips_as_json(**kwargs):
    return json.loads(serializers.serialize("json", get_all_trips(**kwargs)))


def add_trip(values, token):
    trip = Trips(
        owner=users_db.get_user(token=token),
        car=cars_db.get_car(values["car"]),
        price=values["price"],
        departure=values["departure"],
        destination=values["destination"],
        start=values["start"],
        end=values["end"],
    )
    trip.save()


def delete_trip(token: str, id_: int):
    user = users_db.get_user(token=token)
    trip = get_target_trip(id=id_)
    flag = trip.owner == user
    if flag:
        trip.delete()
    return flag


def get_target_trip(**kwargs) -> Trips:
    return Trips.objects.filter(
        **kwargs
    ).first()


def get_trips(token):
    user = users_db.get_user(token=token)
    return Trips.objects.filter(owner=user).all()


def get_trips_as_json(token):
    return json.loads(serializers.serialize("json", get_trips(token)))


def is_exists(id_):
    try:
        trip = get_target_trip(id=id_)
        return trip.id
    except Exception:
        return False