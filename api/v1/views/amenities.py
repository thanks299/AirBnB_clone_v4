#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""


from flask import request
from flask import abort
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """attains the list of all Amenity obj"""
    amenities = [amenity.to_dict()
                 for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """attains Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")
    return jsonify(amenity.to_dict())


@app_views.route('/amenities',
                 methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates amenity"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    amenity = Amenity(**request.json)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates Amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")
    if not request.json:
        abort(400, 'Not a JSON')
    for k, val in request.json.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
