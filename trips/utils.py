from django.db.models import QuerySet


def filter_by_gender(all_trips: QuerySet, gender) -> list:
    return list(
        filter(
            lambda trip: trip.owner.gender == gender, all_trips
        )
    )


def filter_by_departure(trip_departure, departure):
    if departure["district"] != trip_departure.district:
        return False
    if departure["name"] != trip_departure.name:
        return False
    if departure["subject"] != trip_departure.subject:
        return False
    return True


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
