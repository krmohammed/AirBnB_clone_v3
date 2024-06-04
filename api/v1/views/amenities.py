#!/usr/bin/python3
""" Amenity views """
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    all_amenities = storage.all(Amenity)
    amenities = [am.to_dict() for am in all_amenities.values()]
    return jsonify(amenities)


@app_views.route("/amenities/<ame_id>", methods=["GET"], strict_slashes=False)
def get_amenity(ame_id):
    """ Retrieves an Amenity object """
    amenity = storage.get(Amenity, ame_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amId>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amId):
    """ Deletes an Amenity object """
    amenity = storage.get(Amenity, amId)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """ Creates an Amenity """
    if not request.is_json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    info = request.get_json()
    new_amenity = Amenity(**info)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<ame_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(ame_id):
    """ Updates an Amenity object """
    amenity = storage.get(Amenity, ame_id)
    if not amenity:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
