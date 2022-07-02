from trips.models import Trips
from django.core import serializers
import json
import users.db_communication as db


def get_all_trips(**kwargs):
    Trips.objects.filter(**kwargs).all()


def get_all_trips_as_json(**kwargs):
    return json.loads(serializers.serialize("json", get_all_trips(**kwargs)))


def add_trip(values, token):
    user = db.get_user(token=token)
    trip = Trips(
        owner=user,
        car=values("car"),
        price=values("price"),
        departure=values("departure"),
        destination=values("destination"),
        start=values("start"),
        end=values("end"),
    )
    trip.save()
    return trip.objects.values()
