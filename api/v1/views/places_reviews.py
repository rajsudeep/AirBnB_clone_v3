#!/usr/bin/python3
""" reviews module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_places_by_place_id(place_id):
    """ retrieves the list of Review objs """
    obj = storage.get("Place", place_id)
    if not obj:
        abort(404)
    new_dict = [obj.to_dict() for obj in storage.all(Review).values()
                if obj.place_id == place_id]
    return jsonify(new_dict)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ retrieves the review object """
    obj = storage.get("Review", review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ deletes the review obj """
    obj = storage.get("Review", review_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """ creates review obj """
    if not storage.get("Place", place_id):
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    elif 'user_id' not in req:
        abort(400, "Missing user_id")
    elif not storage.get('User', req['user_id']):
        abort(404)
    elif 'text' not in req:
        abort(400, "Missing text")
    req["place_id"] = place_id
    obj = Review(**req)
    storage.new(obj)
    storage.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ updates review obj """
    obj = storage.get("Review", review_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k not in ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(obj, k, v)
    storage.save()
    return make_response(obj.to_dict(), 200)
