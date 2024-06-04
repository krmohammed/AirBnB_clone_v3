#!/usr/bin/python3
""" States views """
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places", methods=["GET"], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    all_places = storage.all(Place)
    places = []
    for place in all_places.values():
        if place.city_id == city_id:
            places.append(place.to_dict())
    if not places:
        abort(404)
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"], strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    from models.city import City
    from models.user import User

    if not storage.get(City, city_id):
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    if "name" not in request.json:
        abort(400, description="Missing name")
    if "user_id" not in request.json:
        abort(400, description="Missing user_id")
    info = request.get_json()
    if not storage.get(User, info["user_id"]):
        abort(404)
    new_place = Place(**info)
    setattr(new_place, "city_id", city_id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200
