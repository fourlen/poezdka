from trips.models import Trips
from django.core import serializers
import json
import users.db_communication as users_db
import cars.db_communication as cars_db
import booking.db_communication as booking_db
import time


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
    return list(
        filter(
            lambda x: time.time() - x.end < 0,
            Trips.objects.filter(owner=user).all()
        )
    )


def get_trips_as_json(token):
    return json.loads(serializers.serialize("json", get_trips(token)))


def get_past_trips(token):
    user = users_db.get_user(token=token)
    return list(
        filter(
            lambda x: time.time() - x.end > 0,
            Trips.objects.filter(owner=user).all()
        )
    )


def get_past_trips_as_json(token):
    return json.loads(serializers.serialize("json", get_past_trips(token)))


def get_all_booking(token):
    user = users_db.get_user(token=token)
    return booking_db.get_all_booking(owner=user)


def get_booked_trips(token):
    all_booking = get_all_booking(token)
    return list(
        filter(
            lambda x: time.time() - x.end < 0,
            [Trips.objects.get(id=i.trip_id) for i in all_booking]
        )
    )


def get_booked_trips_as_json(token):
    return json.loads(serializers.serialize("json", get_booked_trips(token)))


def get_past_booked_trips(token):
    all_booking = get_all_booking(token)
    return list(
        filter(
            lambda x: time.time() - x.end > 0,
            [Trips.objects.get(id=i.trip_id) for i in all_booking]
        )
    )


def get_past_booked_trips_as_json(token):
    return json.loads(serializers.serialize("json", get_past_booked_trips(token)))


def is_exists(id_):
    try:
        trip = get_target_trip(id=id_)
        return trip.id
    except Exception:
        return False
