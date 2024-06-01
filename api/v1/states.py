#!/usr/bin/env python3

# Betty comments (code explanations)

from flask import Flask, jsonify, request
import uuid  # For generating unique state IDs
from datetime import datetime  # For timestamps

# Flask application initialization
app = Flask(__name__)

# State class to represent a state object
class State:
    def __init__(self, name):
        self.id = uuid.uuid4()
        self.name = name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    new_state_name = data.get("name")
if new_state_name:
    new_state = State(new_state_name)
    states.append(new_state)

# List to store states (replace with database interaction for persistence)
states = []

# API endpoint to create a new state (POST /api/v1/states)
@app.route("/api/v1/states", methods=["POST"])
def create_state():
    # Get request data as a dictionary (using request.get_json)
    data = request.get_json()

    # Validate request body for missing "name" key and invalid JSON
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    # Create a new state object with the provided name
    new_state = State(data["name"])

    # Add the new state to the list (replace with database operation)
    states.append(new_state)

    # Return the newly created state object with status code 201 (Created)
    return jsonify(new_state), 201

# API endpoint to update an existing state (PUT /api/v1/states/<state_id>)
@app.route("/api/v1/states/<int:state_id>", methods=["PUT"])
def update_state(state_id):
    # Find the state object with the matching ID
    state = next((s for s in states if s.id == state_id), None)

    # Handle state not found error (404 Not Found)
    if not state:
        return jsonify({"error": "State not found"}), 404

    # Get request data as a dictionary (using request.get_json)
    data = request.get_json()

    # Validate request body for invalid JSON
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    # Update state attributes (ignoring id, created_at, and updated_at)
    for key, value in data.items():
        if key in ["id", "created_at", "updated_at"]:
            continue
        setattr(state, key, value)

    # Update the updated_at timestamp
    state.updated_at = datetime.utcnow()

    # Return the updated state object with status code 200 (OK)
    return jsonify(state), 200

if __name__ == "__main__":
    app.run(debug=True)
