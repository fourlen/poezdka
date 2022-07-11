http://194.87.145.140/:
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
            response
            {
                "success": bool,
                "status": str,
            }
        delete<int::id>/:
            DELETE
            request:
                Headers:
                    "Authorisation": str
            response
            {
                "success": bool,
                "status": str,
            }
	get_trips/:
            GET
            request:
                Headers:
                    "Authorisation": str
            response
		{
    		"trips": [
        		{
            		"model": str,
            		"pk": id,
            		"fields": {
                		"owner": int,
                		"car": int,
                		"price": int,
                		"departure": str,
                		"destination": str,
                		"start": int,
                		"end": int
            			}
        		}
    		]}
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
        delete<int::id>/:
            DELETE
            request:
                Headers:
                    "Authorisation": str
            response
            {
                "success": bool,
                "status": str,
            }
	get_cars/:
            GET
            request:
                Headers:
                    "Authorisation": str
            response
		{
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
    		]}
