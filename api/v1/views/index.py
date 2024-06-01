#!/usr/bin/python3
"""API index view"""


from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def attain_status():
    """Attain API status"""
    return jsonify(status='OK')


@app_views.route('/stats')
def attain_stats():
    """Attain the number of each object by type"""
    info = {
        "amenities": len(storage.all("Amenity")),
        "cities": len(storage.all("City")),
        "places": len(storage.all("Place")),
        "reviews": len(storage.all("Review")),
        "states": len(storage.all("State")),
        "users": len(storage.all("User"))
    }
    return jsonify(info)
