from models import Trips
from django.core import serializers
import json

def get_all_trips(**kwargs):
    Trips.objects.filter(**kwargs).all()


def get_all_trips_as_json(**kwargs):
    return json.loads(serializers.serialize("json", get_all_trips(**kwargs)))
