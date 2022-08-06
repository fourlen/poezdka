from cars.models import Auto
import users.db_communication as users_db


def add_car(values: dict, token: str):
    car = Auto(
        owner=users_db.get_user(token=token),
        mark=values["mark"],
        model=values["model"],
        color=values["color"],
        vehicle_number=values["vehicle_number"],
    )
    try:
        if values["count_of_passengers"]:
            car.count_of_passengers = values["count_of_passengers"]
    except KeyError:
        pass
    car.save()


def delete_car(token: str, id_: int):
    user = users_db.get_user(token=token)
    car = Auto.objects.get(id=id_)
    flag = car.owner == user
    if flag:
        car.delete()
    return flag


def get_car(id_: int):
    return Auto.objects.get(id=id_)


def get_all_cars(token):
    user = users_db.get_user(token=token)
    return Auto.objects.filter(owner=user).all()


def get_all_cars_as_json(token):
    return [get_car_as_json(car) for car in get_all_cars(token)]


def get_car_as_json(car):
    return {
        'pk': car.id,
        'owner': car.owner.id,
        'mark': car.mark,
        'model': car.model,
        'color': car.color,
        'vehicle_number': car.vehicle_number,
        'count_of_passengers': car.count_of_passengers
    }
