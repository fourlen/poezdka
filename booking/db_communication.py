from booking.models import *
from users import db_communication as users_db
from trips import db_communication as trips_db
from booking.exceptions import *
import asyncio


def book(token, id_, seats) -> int:
    trip = trips_db.get_target_trip(id=id_)
    if not trips_db.is_exists(id_):
        raise NotExistException
    user = users_db.get_user(token=token)
    if trip.owner == user:
        raise AlreadyInTripException
    for seat in seats:
        if seat in get_taken_seats(trips_db.get_target_trip(id=id_)):
            raise SeatIsTakenException
    booking = Booking(
        owner=users_db.get_user(token=token),
        trip=trip
    )
    booking.set_seat(seats)

    # asyncio.run(trips_db.notify(trip.owner.id, 'new booking'))
    booking.save()
    return booking.id


def cancel_booking(token: str, id_: int):
    user = users_db.get_user(token=token)
    booking = Booking.objects.get(owner=user, trip=trips_db.get_target_trip(id=id_))
    if not booking:
        raise NotExistException
    flag = booking.owner == user
    if flag:
        booking.delete()
    asyncio.run(trips_db.notify(booking.owner.id, 'cancel booking'))
    return flag


def get_passengers(id_: int):
    return list(set([
        i.owner for i in Booking.objects.filter(trip_id=id_).all()
    ]))


def get_passengers_and_bookings(id_: int):
    return [
        (i.owner, i.id) for i in Booking.objects.filter(trip_id=id_).all()
    ]


def get_user_seat(user, trip):
    list_ = []
    for i in get_passengers_and_bookings(trip.id):
        if i[0] == user:
            list_.extend(get_booking(id=i[1]).get_seat())
    if list_:
        return list_
    else:
        raise NotInTripException

def get_taken_seats(trip):
    taken = []
    for booking in Booking.objects.filter(trip=trip):
        taken.extend(booking.get_seat())
    return taken


def get_booking(**kwargs) -> Booking:
    return Booking.objects.filter(
        **kwargs
    ).first()


def get_all_booking(owner):
    return Booking.objects.filter(
        owner=owner
    ).all()
