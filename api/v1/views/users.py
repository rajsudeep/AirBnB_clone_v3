#!/usr/bin/python3
""" users module """
from api.v1.views import app_views
from flask import Flask, jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """ retrieves the list of user objs """
    new_dict = [v.to_dict() for v in storage.all(User).values()]
    return jsonify(new_dict)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ retrieves specific user """
    obj = storage.get("User", user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ deletes specific user """
    obj = storage.get("User", user_id)
    if not obj:
        abort(404)
    storage.delete(obj)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """ creates a new user """
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    if 'email' not in req:
        abort(400, "Missing email")
    if 'password' not in req:
        abort(400, "Missing password")
    obj = User(**req)
    storage.new(obj)
    storage.save()
    return make_response(obj.to_dict(), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ update specified state """
    obj = storage.get("User", user_id)
    if not obj:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for k, v in req.items():
        if k is not "id" or "email" or "created_at" or "updated_at":
            setattr(obj, k, v)
    storage.save()
    return make_response(obj.to_dict(), 200)
