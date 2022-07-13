from booking.models import *
from users import db_communication as users_db
from trips import db_communication as trips_db
from booking.exceptions import *


def book(token, id_) -> int:
    trip = trips_db.get_target_trip(id=id_)
    if not trips_db.is_exists(id_):
        raise NotExistException
    user = users_db.get_user(token=token)
    if (user in get_passengers(id_)) or (trip.owner == user):
        raise AlreadyInTripException
    if user in get_banned_users(id_):
        raise BannedUserException
    booking = Booking(
        owner=users_db.get_user(token=token),
        trip=trip
    )
    booking.save()
    return booking.id


def cancel_booking(token: str, id_: int):
    user = users_db.get_user(token=token)
    booking = get_booking(id=id_)
    if not booking:
        raise NotExistException
    flag = booking.owner == user
    if flag:
        ban_user(user, booking)
        booking.delete()
    return flag


def get_passengers(id_: int):
    return [
        i.owner for i in Booking.objects.filter(trip_id=id_).all()
    ]


def get_banned_users(id_: int):
    return [
        i.user for i in BannedUsers.objects.filter(trip_id=id_).all()
    ]


def get_booking(**kwargs) -> Booking:
    return Booking.objects.filter(
        **kwargs
    ).first()


def ban_user(user, booking: Booking):
    ban = BannedUsers(
        user=user,
        trip=trips_db.get_target_trip(id=booking.trip_id)
    )
    ban.save()
