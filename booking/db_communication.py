from booking.models import *
from users import db_communication as users_db
from trips import db_communication as trips_db
from booking.exceptions import *
import asyncio
from loguru import logger


def book(token, id_, seats) -> int:
    trip = trips_db.get_target_trip(id=id_)
    if not trips_db.is_exists(id_):
        raise NotExistException
    if seats:
        for seat in seats:
            if seat in get_taken_seats(trips_db.get_target_trip(id=id_)):
                raise SeatIsTakenException
        booking = Booking(
            owner=users_db.get_user(token=token),
            trip=trip
        )
        booking.set_seat(seats)
    else:
        booking = Booking(
            owner=users_db.get_user(token=token),
            trip=trip
        )
    if seats:
        trips_db.push_notify(trip.owner.fcm_token, 'Поездка', f'У вас новая бронь. Поездка'
                                                              f' {trip.departure_set.first().name}-'
                                                              f'{trip.stops_set.last().name}')
    else:
        trips_db.push_notify(trip.owner.fcm_token, 'Поездка', f'Бронирование передачи посылки. Поездка'
                                                              f' {trip.departure_set.first().name}-'
                                                              f'{trip.stops_set.last().name}')
    asyncio.run(trips_db.notify(trip.owner.id, 'new booking'))
    booking.save()
    return booking.id


def cancel_booking(token: str, id_: int):
    user = users_db.get_user(token=token)
    bookings = Booking.objects.filter(owner=user, trip=trips_db.get_target_trip(id=id_))
    if not bookings:
        raise NotExistException
    for booking in bookings:
        booking.delete()
    trips_db.push_notify(user.fcm_token, 'cancel booking', 'cancel booking')
    asyncio.run(trips_db.notify(booking.trip.owner.id, 'cancel booking'))
    return True


def cancel_booking_for_driver(token: str, trip_id: int, user_id):
    driver = users_db.get_user(token=token)
    user = users_db.get_user(id=user_id)
    trip = trips_db.get_target_trip(id=trip_id)
    if trip.owner != driver:
        raise Exception('Khui tebe')
    bookings = Booking.objects.filter(owner_id=user_id, trip=trip)
    for booking in bookings:
        booking.delete()
    trips_db.push_notify(user.fcm_token, 'cancel booking', 'cancel booking')
    asyncio.run(trips_db.notify(user.id, 'cancel booking'))
    return True


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
