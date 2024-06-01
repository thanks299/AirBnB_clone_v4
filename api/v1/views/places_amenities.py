#!/usr/bin/python3
"""
Place objects and Amenity objects
that handles all default RESTFul API actions
"""


from flask import request
from flask import abort
from flask import jsonify
from api.v1.views import app_views
from models.place import Place
from models.amenity import Amenity
from models import storage


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def get_place_amenities(place_id):
    """attain the list of all Amenity obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    if storage.__class__.__name__ == 'DBStorage':
        amenities = [amenity.to_dict() for amenity in place.amenities]
    else:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in place.amenity_ids]
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """Deletes amenity obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")
    if amenity not in place.amenities:
        abort(404, "Amenity is not linked to the Place")
    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """Links amenity obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404, "Amenity not found")
    if storage.__class__.__name__ == 'DBStorage':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    storage.save()
    return jsonify(amenity.to_dict()), 201
