#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions"""


from flask import request, abort, jsonify
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """attains the list of all Place obj"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not found")
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """attains place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, "City not found")
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    user_id = request.json['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")
    request.json['city_id'] = city_id
    place = Place(**request.json)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    if not request.json:
        abort(400, 'Not a JSON')
    for k, val in request.json.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, k, val)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes place obj"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places_search',
                 methods=['POST'], strict_slashes=False)
def search_places():
    """search places based on State, City, or Amenity"""
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, description='Not a JSON')

    all_places = storage.all(Place).values()
    places = []
    places_id = []

    k_info = {
        'states': data.get('states', []),
        'cities': data.get('cities', []),
        'amenities': data.get('amenities', [])
    }

    if k_info['states']:
        for state_id in k_info['states']:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    new_places = [place for place in city.places
                                  if place.id not in places_id]
                    places.extend(new_places)
                    places_id.extend([place.id for place in new_places])

    if k_info['cities']:
        for city_id in k_info['cities']:
            city = storage.get(City, city_id)
            if city:
                new_places = [place for place in city.places
                              if place.id not in places_id]
                places.extend(new_places)
                places_id.extend([place.id for place in new_places])

    if not k_info['states'] and not k_info['cities']:
        places = all_places
    if k_info['amenities']:
        amenity_ids = set()
        for amenity_id in k_info['amenities']:
            amenity = storage.get(Amenity, amenity_id)
            if amenity:
                amenity_ids.add(amenity_id)

        diff_pl = []
        for place in places:
            place_amenities_ids = {amenity.id for amenity in place.amenities}
            if amenity_ids.issubset(place_amenities_ids):
                diff_pl.append(place)
        places = diff_pl

    result = [place.to_dict() for place in places]
    return jsonify(result)
