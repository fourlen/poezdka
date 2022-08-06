from django.db.models import QuerySet


def filter_by_conditioner_and_gender(all_trips: QuerySet, gender) -> list:
    return list(
        filter(
            lambda trip: trip.car.conditioner is True and
            trip.owner.gender == gender, all_trips
        )
    )


def filter_by_departure(trip_departure, departure):
    return departure["district"] == trip_departure.district\
        and departure["name"] == trip_departure.name\
        and departure["subject"] == trip_departure.subject


def filter_by_destination(stops, destination):
    for stop in stops:
        if destination["district"] != stop.district:
            continue
        if destination["name"] != stop.name:
            continue
        if destination["subject"] != stop.subject:
            continue
        return True
    return False

