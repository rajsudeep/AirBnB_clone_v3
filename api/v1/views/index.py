#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ gets the status """
    return jsonify({"status": "OK"})

