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
    user = users_db.get_user(token=token)
    trip = Trips(
        owner=user,
        car=cars_db.get_car(values["car"]),
        price=values["price"],
        departure=values["departure"],
        destination=values["destination"],
        start=values["start"],
        end=values["end"],
    )
    trip.save()


def get_trips(token):
    user = users_db.get_user(token=token)
    return Trips.objects.filter(owner=user).all()


def get_trips_as_json(token):
    return json.loads(serializers.serialize("json", get_trips(token)))
