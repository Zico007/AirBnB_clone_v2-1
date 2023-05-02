#!/usr/bin/python3
"""This returns the status of our api"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<string:place_id>/amenities',
                 strict_slashes=False, methods=['GET'])
def get_all_place_amenities(place_id):
    """This performs various tasks according to
    the request received
    GET: Return all the amenities in a place"""
    val = storage.get(cls=Place, id=place_id)
    if not val:
        abort(404)
    return jsonify([x.to_dict() for x in val.amenities])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE', 'POST'])
def work_with_ids(place_id, amenity_id):
    """This plays on the reationships between an place and
    an amenity
    DELETE: removes that relationship
    POST: Creates that relationship"""
    val = storage.get(cls=Place, id=place_id)
    amen = storage.get(cls=Amenity, id=amenity_id)
    if val is None or amen is None:
        abort(404)
    if request.method == 'POST':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amen in val.amenites:
                return make_response(jsonify(amen.to_dict()), 200)
            val.amenities.append(amen)
        else:
            if amen.id in val.amenity_ids:
                return make_response(jsonify(amen.to_dict()), 200)
            val.amenity_ids.append(amenity_id)
        storage.save()
        return make_response(jsonify(amen.to_dict()), 201)
    elif request.method == 'DELETE':
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            if amen not in place.amenites:
                abort(404)
            val.amenities.remove(amen)
        else:
            if amen.id not in val.amenity_ids:
                abort(404)
            val.amenity_ids.remove(amenity_id)
        storage.save()
        return make_response(jsonify({}), 200)
