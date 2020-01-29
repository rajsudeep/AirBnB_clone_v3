#!/usr/bin/python3
""" amenity module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ retrieves the list of amenity objs """
    new_dict = [v.to_dict() for v in storage.all(Amenity).values()]
    return jsonify(new_dict)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ retrieves specific amenity """
    obj = storage.get("Amenity", amenity_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletes specific amenity """
    obj = storage.get("Amenity", amenity_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """ creates a new amenity """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if 'name' not in req:
        abort(400, "Missing name")
    obj = Amenity(**req)
    storage.new(obj)
    storage.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ update specified amenity """
    obj = storage.get("Amenity", amenity_id)
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
