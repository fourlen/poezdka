from booking.models import *
from users import db_communication as users_db
from trips import db_communication as trips_db
from booking.exceptions import *
import asyncio


def book(token, id_, seat) -> int:
    trip = trips_db.get_target_trip(id=id_)
    if not trips_db.is_exists(id_):
        raise NotExistException
    user = users_db.get_user(token=token)
    if (user in get_passengers(id_)) or (trip.owner == user):
        raise AlreadyInTripException
    if user in get_banned_users(id_):
        raise BannedUserException
    if seat in get_taken_seats(trips_db.get_target_trip(id=id_)):
        raise SeatIsTakenException
    owner = users_db.get_user(token=token)
    booking = Booking(
        owner=owner,
        trip=trip,
        seat=seat
    )
    asyncio.run(trips_db.notify(owner.id, 'new booking'))
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
    asyncio.run(trips_db.notify(booking.owner.id, 'cancel booking'))
    return flag


def get_passengers(id_: int):
    return [
        i.owner for i in Booking.objects.filter(trip_id=id_).all()
    ]


def get_user_seat(user, trip):
    if user not in get_passengers(trip.id):
        raise NotInTripException
    return get_booking(owner=user).seat


def get_taken_seats(trip):
    return list(
        map(
            lambda x: get_user_seat(x, trip), get_passengers(trip.id)
        )
    )


def get_banned_users(id_: int):
    return [
        i.user for i in BannedUsers.objects.filter(trip_id=id_).all()
    ]


def get_booking(**kwargs) -> Booking:
    return Booking.objects.filter(
        **kwargs
    ).first()


def get_all_booking(owner):
    return Booking.objects.filter(
        owner=owner
    ).all()


def ban_user(user, booking: Booking):
    ban = BannedUsers(
        user=user,
        trip=trips_db.get_target_trip(id=booking.trip_id)
    )
    ban.save()
