#!/usr/bin/python3
"""User object that handles all default RESTFul API actions"""


from flask import request
from flask import abort
from flask import jsonify
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_users():
    """attains the list of all User obj"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """attains User obj"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")
    return jsonify(user.to_dict())


@app_views.route('/users',
                 methods=['POST'], strict_slashes=False)
def create_user():
    """Creates User"""
    if not request.json:
        abort(400, 'Not a JSON')
    if 'email' not in request.json:
        abort(400, 'Missing email')
    if 'password' not in request.json:
        abort(400, 'Missing password')
    user = User(**request.json)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates User obj"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")
    if not request.json:
        abort(400, 'Not a JSON')
    for k, val in request.json.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, val)
    storage.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes User obj"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404, "User not found")
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
