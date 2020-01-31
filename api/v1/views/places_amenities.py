#!/usr/bin/python3
""" place_amenities module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_places_by_amenity(place_id):
    """ retrieves the list of Amenity objs """
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    new_dict = [obj.to_dict() for obj in storage.all(Amenity).values()
                if obj.place_id == place_id]
    return jsonify(new_dict)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_by_place(place_id, amenity_id):
    """ deletes the amenity obj """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if amenity.place_id == place_id:
        place.amenities.remove(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_amenity_by_place(place_id):
    """ creates amenity obj """
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if amenity.place_id == place_id:
        return make_response(amenity.to_dict(), 200)
    else:
        place.amenities.append(amenity)
        storage.save()
        return make_response(obj.to_dict(), 201)
