#!/usr/bin/python3
""" Places Reviews views """
from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects"""
    all_reviews = storage.all(Review).values()
    reviews = []
    for review in all_reviews:
        if review.place_id == place_id:
            reviews.append(review.to_dict())
    if not reviews:
        abort(404)
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def post_review(place_id):
    """Creates a Review"""
    from models.city import Place

    if not storage.get(Place, place_id):
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    if "text" not in request.json:
        abort(400, description="Missing text")
    if "user_id" not in request.json:
        abort(400, description="Missing user_id")
    info = request.get_json()
    if not storage.get(User, info['user_id']):
        abort(404)
    new_review = Review(**info)
    setattr(new_review, "place_id", place_id)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
