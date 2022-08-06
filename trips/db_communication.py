from trips.models import *
import users.db_communication as users_db
import cars.db_communication as cars_db
import booking.db_communication as booking_db
import time
import trips.utils as utils


def get_all_trips():
    return Trips.objects.all()


def add_trip(values, token):
    user = users_db.get_user(token=token)
    if not user:
        raise Exception("Unauthorized")
    try:
        car = cars_db.get_car(values["car"])
        if car.owner != user:
            raise Exception("Not your car, hacker")
        trip = Trips(
            owner=user,
            car=car,
            price=values["price"],
            start=values["start"],
        )
    except KeyError:
        trip = Trips(
            owner=user,
            price=values["price"],
            start=values["start"],
        )
    try:
        trip.animals = values["animals"]
    except KeyError:
        pass
    try:
        trip.package = values["package"]
    except KeyError:
        pass
    try:
        trip.baggage = values["baggage"]
    except KeyError:
        pass
    try:
        trip.baby_chair = values["baby_chair"]
    except KeyError:
        pass
    try:
        trip.smoke = values["smoke"]
    except KeyError:
        pass
    try:
        trip.two_places_in_behind = values["two_places_in_behind"]
    except KeyError:
        pass
    try:
        trip.conditioner = values["conditioner"]
    except KeyError:
        pass
    try:
        trip.premium = values["premium"]
    except KeyError:
        pass
    trip.save()
    add_departure(values["departure"], trip)
    for stop in values["stops"]:
        add_stop(stop, trip)


def add_departure(departure: dict, trip: Trips):
    departure = Departure(
        trip=trip,
        lat=departure["coords"]["lat"],
        lon=departure["coords"]["lon"],
        district=departure["district"],
        name=departure["name"],
        population=departure["population"],
        subject=departure["subject"],
    )
    departure.save()


def add_stop(stop: dict, trip: Trips):
    stop = Stops(
        trip=trip,
        lat=stop["coords"]["lat"],
        lon=stop["coords"]["lon"],
        district=stop["district"],
        name=stop["name"],
        distance_to_previous=stop["distance_by_past"],
        population=stop["population"],
        subject=stop["subject"],
        time=stop["time"],
    )
    stop.save()


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
            lambda x: time.time() - x.start < 0,
            Trips.objects.filter(owner=user).all()
        )
    )


def get_trips_as_json(token):
    return [
        pretty_trip(trip) for trip in get_trips(token)
    ]


def get_past_trips(token):
    user = users_db.get_user(token=token)
    return list(
        filter(
            lambda x: time.time() - x.start > 0,
            Trips.objects.filter(owner=user).all()
        )
    )


def get_past_trips_as_json(token):
    return [
        pretty_trip(trip) for trip in get_past_trips(token)
    ]


def get_all_booking(token):
    user = users_db.get_user(token=token)
    return booking_db.get_all_booking(owner=user)


def get_booked_trips(token):
    all_booking = get_all_booking(token)
    return list(
        filter(
            lambda x: time.time() - x.start < 0,
            [Trips.objects.get(id=i.trip_id) for i in all_booking]
        )
    )


def get_booked_trips_as_json(token):
    return [
        pretty_trip(trip) for trip in get_booked_trips(token)
    ]


def get_past_booked_trips(token):
    all_booking = get_all_booking(token)
    return list(
        filter(
            lambda x: time.time() - x.start > 0,
            [Trips.objects.get(id=i.trip_id) for i in all_booking]
        )
    )


def get_past_booked_trips_as_json(token):
    return [
        pretty_trip(trip) for trip in get_past_booked_trips(token)
    ]


def is_exists(id_):
    try:
        trip = get_target_trip(id=id_)
        return trip.id
    except Exception:
        return False


def get_main_future_trips(all_trips):
    print(all_trips)
    return list(
        filter(
            lambda x: x.start - time.time() > 0 and x.car,
            all_trips
        )
    )


def get_drivers_future_trips(all_trips):
    return list(
        filter(
            lambda x: x.start - time.time() > 0 and not x.car,
            all_trips
        )
    )


def filter_trips(values: dict):
    all_trips = get_all_trips()
    try:
        if values["animals"]:
            all_trips = all_trips.filter(
                animals=True
            ).all()
    except KeyError:
        pass
    try:
        if values["package"]:
            all_trips = all_trips.filter(
                package=True
            ).all()
    except KeyError:
        pass
    try:
        if values["baggage"]:
            all_trips = all_trips.filter(
                baggage=True
            ).all()
    except KeyError:
        pass
    try:
        if values["baby_chair"]:
            all_trips = all_trips.filter(
                baby_chair=True
            ).all()
    except KeyError:
        pass
    try:
        if values["smoke"]:
            all_trips = all_trips.filter(
                smoke=True
            ).all()
    except KeyError:
        pass
    try:
        if values["two_places_in_behind"]:
            all_trips = all_trips.filter(
                two_places_in_behind=True
            ).all()
    except KeyError:
        pass
    try:
        if values["conditioner"]:
            all_trips = all_trips.filter(
                conditioner=True
            ).all()
    except KeyError:
        pass
    try:
        if values["owner_gender"]:
            all_trips = utils.filter_by_gender(all_trips, gender=values["owner_gender"])
    except KeyError:
        pass
    return all_trips


def get_filter_trips(values: dict, all_trips):
    copy = []
    packet = values["packet"] if "packet" in values else 0
    for trip in all_trips:
        if "departure" in values and not(
                values["departure"] and
                utils.filter_by_departure(get_departure(trip), values["departure"])):
            continue
        if "destination" in values and not(
                values["destination"] and
                utils.filter_by_departure(get_stops(trip), values["destination"])):
            continue
        copy.append(trip)
    return {
            "all_trips": list(
                map(
                    pretty_trip, get_packet(sorted(
                        copy, key=lambda x: not x.premium
                    ), packet)
                )
            )
        }


def get_packet(trips: list[Trips], i):
    return trips[i * 10: (i + 1) * 10]


def get_departure(trip):
    return Departure.objects.get(trip=trip)


def get_stops(trip):
    return Stops.objects.filter(trip=trip).all()


def pretty_departure(departure: Departure):
    return {
            "coords": {
                "lat": departure.lat,
                "lon": departure.lon,
            },
            "district": departure.district,
            "name": departure.name,
            "population": departure.population,
            "subject": departure.subject,
    }


def pretty_stop(stop: Stops):
    return {
            "coords": {
                "lat": stop.lat,
                "lon": stop.lon,
            },
            "district": stop.district,
            "name": stop.name,
            "population": stop.population,
            "subject": stop.subject,
            "approach_time": stop.time,
            "distance_to_previous": stop.distance_to_previous
    }


def pretty_trip(trip: Trips):
    departure = get_departure(trip)
    stops = get_stops(trip)
    return {
        "is_premium": trip.premium,
        "trip_id": trip.id,
        "owner": users_db.get_user_for_trip(trip.owner),
        "car": cars_db.get_car_as_json(
            trip.car
        ) if trip.car else None,
        "price": trip.price,
        "time_start": trip.start,
        "departure": pretty_departure(departure),
        "stops": [
            pretty_stop(stop) for stop in stops
        ],
        "package": trip.package,
        "baggage": trip.baggage,
        "baby_chair": trip.baby_chair,
        "smoke": trip.smoke,
        "animals": trip.animals,
        "two_places_in_behind": trip.two_places_in_behind,
        "passengers": [users_db.get_user_for_trip(i, trip) for i in booking_db.get_passengers(trip.id)],
        "conditioner": trip.conditioner,
        "owner_gender": trip.owner.gender,
    }
