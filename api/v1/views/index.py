#!/usr/bin/python3
""" index view """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status():
    """Return the status"""
    stattus = {"status": "OK"}
    return stattus


@app_views.route("/stats")
def stats():
    """ Retrieves the number of each objects """
    menu = {
        "amenities": Amenity, "cities": City,
        "places": Place, "reviews": Review,
        "states": State, "users": User
        }
    stats = {k: storage.count(v) for k, v in menu.items()}
    return stats
