"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, Person, Address

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/person', methods=['POST', 'GET'])
def handle_person():
    """
    Create person and retrieve all persons
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'first_name' not in body:
            raise APIException('You need to specify the first_name', status_code=400)
        if 'last_name' not in body:
            raise APIException('You need to specify the last_name', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)

        user1 = Person(username=body['username'], password=body['password'], email=body['email'], first_name=body['first_name'], last_name=body['last_name'], phone=body['phone'])
        db.session.add(user1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_people = Person.query.all()
        all_people = list(map(lambda x: x.serialize(), all_people))
        return jsonify(all_people), 200

    return "Invalid Method", 404


@app.route('/person/<int:person_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_person(person_id):
    """
    Single person
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'username' not in body:
            raise APIException('You need to specify the username', status_code=400)
        if 'password' not in body:
            raise APIException('You need to specify the password', status_code=400)
        if 'email' not in body:
            raise APIException('You need to specify the email', status_code=400)
        if 'first_name' not in body:
            raise APIException('You need to specify the first_name', status_code=400)
        if 'last_name' not in body:
            raise APIException('You need to specify the last_name', status_code=400)
        if 'phone' not in body:
            raise APIException('You need to specify the phone', status_code=400)

        return jsonify(user1.serialize()), 200

    # GET request
    if request.method == 'GET':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        return jsonify(user1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        user1 = Person.query.get(person_id)
        if user1 is None:
            raise APIException('User not found', status_code=404)
        db.session.delete(user1)
        return "ok", 200

    return "Invalid Method", 404

#----------------------------ADDRESS---------------------------------

@app.route('/address', methods=['POST', 'GET'])
def handle_address():
    """
    Create address and retrieve all address
    """

    # POST request
    if request.method == 'POST':
        body = request.get_json()

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'address' not in body:
            raise APIException('You need to specify the address', status_code=400)

        address1 = Person(person_id=body['person_id'], address=body['address'])
        db.session.add(address1)
        db.session.commit()
        return "ok", 200

    # GET request
    if request.method == 'GET':
        all_addresses = Address.query.all()
        all_addresses = list(map(lambda x: x.serialize(), all_addresses))
        return jsonify(all_addresses), 200

    return "Invalid Method", 404


@app.route('/address/<int:address_id>', methods=['PUT', 'GET', 'DELETE'])
def get_single_address(address_id):
    """
    Single address
    """

    # PUT request
    if request.method == 'PUT':
        body = request.get_json()
        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)

        address1 = Address.query.get(address_id)
        if address1 is None:
            raise APIException('address not found', status_code=404)

        if body is None:
            raise APIException("You need to specify the request body as a json object", status_code=400)
        if 'address_id' not in body:
            raise APIException('You need to specify the address id', status_code=400)


        return jsonify(address1.serialize()), 200

    # GET request
    if request.method == 'GET':
        address1 = Address.query.get(address_id)
        if address1 is None:
            raise APIException('Address not found', status_code=404)
        return jsonify(address1.serialize()), 200

    # DELETE request
    if request.method == 'DELETE':
        address1 = Address.query.get(address_id)
        if address1 is None:
            raise APIException('Address not found', status_code=404)
        db.session.delete(address1)
        return "ok", 200

    return "Invalid Method", 404


if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT)
