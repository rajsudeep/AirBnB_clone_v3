#!/usr/bin/python3
""" places module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """ retrieves the list of places """
    obj = storage.get("City", city_id)
    if not obj:
        abort(404)
    new_dict = [v.to_dict() for v in storage.all(Place).values()
                if v.city_id == city_id]
    return jsonify(new_dict)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """ retrieves specific place """
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ deletes specific place """
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ creates a new place """
    if not storage.get("City", city_id):
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if 'user_id' not in req:
        abort(400, "Missing user_id")
    if not storage.get("User", req['user_id']):
        abort(404)
    if 'name' not in req:
        abort(400, "Missing name")
    obj = Place(**req)
    storage.new(obj)
    storage.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """ update specified place """
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for k, v in req.items():
        if k is not ignore:
            setattr(obj, k, v)
    storage.save()
    return make_response(obj.to_dict(), 200)
