class AlreadyInTripException(Exception):
    def __str__(self):
        return "You have already booked this trip, because you are driver"


class NotExistException(Exception):
    def __str__(self):
        return "Trip not found"


class BannedUserException(Exception):
    def __str__(self):
        return "You were forbidden to book this trip"


class NotInTripException(Exception):
    def __str__(self):
        return "The user was not found among the participants of the trip"


class SeatIsTakenException(Exception):
    def __str__(self):
        return "This place is occupied"
