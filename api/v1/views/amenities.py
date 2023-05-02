#!/usr/bin/python3
"""This returns the status of our api"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def work_with_amenities():
    """This performs various tasks according to
    the request received
    GET: Return all Amenity
    POST: Create a new Amenity"""
    if request.method == "GET":
        return jsonify([x.to_dict() for x in storage.all(Amenity).values()])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in data:
            return make_response(jsonify("Missing name"), 400)
        new_amen = Amenity(**data)
        new_amen.save()
        return make_response(jsonify(new_amen.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def work_with_amenity_id(amenity_id):
    """This function performs various tasks according to the
    request received
    GET: Return the desired Amenity
    DELETE: Delete the given Amenity
    PUT: Update the given Amenity"""
    val = storage.get(cls=Amenity, id=amenity_id)
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
            if k not in ['id', 'created_at', 'updated_at']:
                setattr(val, k, v)
        val.save()
        return make_response(jsonify(val.to_dict()), 200)
