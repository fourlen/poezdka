from cars.models import Auto
import users.db_communication as users_db


def add_car(token: str, mark=None, model=None, color=None,
            vehicle_number=None, count_of_passengers=None):
    car = Auto(owner=users_db.get_user(token=token), mark=mark, model=model, color=color,
               vehicle_number=vehicle_number, count_of_passengers=count_of_passengers)
    car.save()


def delete_car(token: str, id_: int):
    user = users_db.get_user(token=token)
    car = Auto.objects.get(id=id_)
    flag = car.owner is user
    if flag:
        car.delete()
    return flag
