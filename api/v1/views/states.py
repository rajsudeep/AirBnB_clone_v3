#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """ retrieves the lise of state objs """
    new_dict = [v.to_dict() for v in storage.all(State).values()]
    return jsonify(new_dict)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ retrieves specific state """
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ deletes specific state """
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    """ creates a new state """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    obj = State(**req)
    storage.new(obj)
    storage.save()
    return make_response(obj.to_dict(), 201)
    
@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """ update specified state """
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k is not "id" or "created_at" or "updated_at":
            setattr(obj, k, v)
    storage.save()
    return make_response(obj.to_dict(), 200)
