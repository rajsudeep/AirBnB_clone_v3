#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """ retrieves the list of city objs """
    obj = storage.get("State", state_id)
    if not obj:
        abort(404)
    new_dict = [obj.to_dict() for obj in storage.all(City).values()
                if obj.state_id == state_id]
    return jsonify(new_dict)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ retrieves the city object """
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    if not storage.get("State", state_id):
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    req["state_id"] = state_id
    obj = City(**req)
    storage.new(obj)
    storage.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k is not "id" or "state_id" or "created_at" or "updated_at":
            setattr(obj, k, v)
    storage.save()
    return make_response(obj.to_dict(), 200)
