#!/usr/bin/python3i
"""This returns the status of our api"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_all_state_cities(state_id):
    """This performs various tasks according to
    the request received
    GET: Return all cities of a state"""
    val = storage.get(cls=State, id=state_id)
    if not val:
        abort(404)
    if request.method == 'GET':
        return jsonify([x.to_dict() for x in val.cities])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in data:
            return make_response(jsonify("Missing name"), 400)
        data['state_id'] = state_id
        city = City(**data)
        city.save()
        return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def work_with_city_id(city_id):
    """This function performs various tasks according to the
    request received
    GET: Return the desired State
    DELETE: Delete the given State
    PUT: Update the given state"""
    val = storage.get(cls=City, id=city_id)
    if not val:
        abort(404)
    if request.method == 'GET':
        return jsonify(val.to_dict())
    elif request.method == "DELETE":
        val.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        for k, v in data.items():
            if k not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(val, k, v)
        val.save()
        return make_response(jsonify(val.to_dict()), 200)
