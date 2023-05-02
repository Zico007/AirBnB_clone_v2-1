#!/usr/bin/python3
"""This returns the status of our api"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State


@app_views.route('/cities/<string:city_id>/places',
                 strict_slashes=False, methods=['GET', 'POST'])
def get_all_city_places(city_id):
    """This performs various tasks according to
    the request received
    GET: Return all places in a city
    POST: Create/add a new place"""
    val = storage.get(cls=City, id=city_id)
    if not val:
        abort(404)
    if request.method == 'GET':
        return jsonify([x.to_dict() for x in val.places])
    elif request.method == 'POST':
        data = request.get_json()
        if data is None:
            return make_response(jsonify("Not a JSON"), 400)
        if 'name' not in data:
            return make_response(jsonify("Missing name"), 400)
        data['city_id'] = city_id
        place = Place(**data)
        place.save()
        return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'PUT', 'DELETE'])
def work_with_place_id(place_id):
    """This function performs various tasks according to the
    request received
    GET: Return the desired place
    DELETE: Delete the given place
    PUT: Update the given place"""
    val = storage.get(cls=Place, id=place_id)
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
            if k not in ['id', 'user_id', 'city_id',
                         'created_at', 'updated_at']:
                setattr(val, k, v)
        val.save()
        return make_response(jsonify(val.to_dict()), 200)


@app_views.route('/places_search', strict_slashes=False, methods=['POST'])
def place_search():
    """ search places by id """
    data = request.get_json()
    if data is None:
        return make_response(jsonify("Not a valid JSON"), 400)
    cities = data.get('cities', None)
    states = data.get('states', None)
    amen_s = data.get('amenities', None)
    if not data or not len(data) or (
            not states and
            not cities and
            not amen_s):
        return jsonify([x.to_dict() for x in storage.all(Place).values()])
    f_places = []
    if states:
        l_states = [storage.get(State, s_id) for s_id in states]
        for state in l_states:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            f_places.append(place)
    if cities:
        l_cities = [storage.get(City, c_id) for c_id in cities]
        for city in l_cities:
            if city:
                for place in city.places:
                    f_places.append(place)
    f_places = [x for x in f_places if x is not None]
    if amen_s:
        l_amen_s = [storage.get(Amenity, a_id) for a_id in amen_s]
        if not f_places:
            f_places = storage.all(Place).values()
        l_amen = [x for x in l_amen_s if x is not None]
        f_places = [x for x in f_places if all(
            mem in x.amenities for mem in l_amen)]
    places = []
    for place in f_places:
        dict_ = place.to_dict()
        dict_.pop('amenities', None)
        places.append(dict_)
    return jsonify(places)
