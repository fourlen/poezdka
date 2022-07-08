http://ystories.site:70/:
    user/:
        registration/:
            POST
            request
            {
                "login": str,
                "password"" str,
                "firstname": str,
                "lastname": str,
                "gender": str ("male" or "female"),
                "birth": int (timestamp)
            }
            response
            {
                "token": token
            }
        auth/:
            POST
            request
            {
                'login': str,
                'password': str
            }
            response:
            {
                'authorized': bool,
                'token': str (if authorized)
                'error': str (if not authorized)
            }
        delete_user/:
            DELETE
            request:
                Headers:
                    "Authorisation": str
            response
            {
                success: True if success else Server error
            }
        get_user/:
            GET
            request:
                Headers:
                    "Authorisation": str
            response
            {
                "token": str,
                "login": str,
                "firstname": str,
                "lastname": str,
                "gender": str,
                "birth": int (timestamp),
                "cars": [{
                    "model": string,
                    "pk": int,
                    "fields": {
                        "owner": int,
                        "mark": str,
                        "model": str,
                        "color": str,
                        "vehicle_number": str,
                        "count_of_passengers": int
                }]
            }
        update_user/:
            PUT
            request:
                Headers:
                    "Authorisation": str
                body:
                    "firstname": str,
                    "lastname": str,
                    "gender": str,
                    "birth": int (timestamp),
            response
            {
                "login": str,
                "firstname": str,
                "lastname": str,
                "gender": str,
                "birth": int (timestamp),
                "cars": [{
                    "model": string,
                    "pk": int,
                    "fields": {
                        "owner": int,
                        "mark": str,
                        "model": str,
                        "color": str,
                        "vehicle_number": str,
                        "count_of_passengers": int
                }]
            }
    trips/:
        add_trip/:
            POST
            request:
                Headers:
                    "Authorisation": str
                body:
                    "car: int,
                    "price": int,
                    "departure": str,
                    "destination": str,
                    "start": int (Timestamp),
                    "end": int (Timestamp),
            response:
                body:
                    "owner": int,
                    "car": int,
                    "price": int,
                    "departure": str,
                    "destination": str,
                    "start": int (Timestamp),
                    "end": int (Timestamp),
    cars/:
        add/:
            request:
                Headers:
                    "Authorisation": str
                body:
                     "mark": str,
                     "model": str,
                     "color": str,
                     "vehicle_number": str,
                     "count_of_passengers": int
            response
            {
                "success": bool,
                "status": str,
            }
        delete_car<int::id>/:
            DELETE
            request:
                Headers:
                    "Authorisation": str
            response
            {
                "success": bool,
                "status": str,
            }
