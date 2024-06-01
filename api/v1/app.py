#!/usr/bin/python3
"""Contains a Flask web application API."""


import os
from flask import Flask
from flask import *
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_flask(exception):
    """App/request context end event listener."""
    storage.close()


@app.errorhandler(404)
def error_404(error):
    """404 HTTP error code"""
    return jsonify(error='Not found'), 404


if __name__ == '__main__':
    app.run(os.getenv("HBNB_API_HOST"), os.getenv("HBNB_API_PORT"))
