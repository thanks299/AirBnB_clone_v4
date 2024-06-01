#!/usr/bin/python3
"""Review object that handles all default RESTFul API actions"""


from flask import request
from flask import abort
from flask import jsonify
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """attains the list of all review obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """attains review obj"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, "Review not found")
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'text' not in request.json:
        abort(400, 'Missing text')
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")
    request.json['place_id'] = place_id
    review = Review(**request.json)
    storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates review object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, "Review not found")
    if not request.json:
        abort(400, 'Not a JSON')
    for k, val in request.json.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, val)
    storage.save()
    return jsonify(review.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Deletes review obj"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, "Review not found")
    storage.delete(review)
    storage.save()
    return jsonify({}), 200
