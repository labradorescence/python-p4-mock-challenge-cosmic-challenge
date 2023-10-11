#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return ''

#app.py

# Define a Flask resource for handling requests related to scientists.
class Scientists(Resource):
    def get(self):
        # Retrieve a list of scientists from the database and apply serialization rules.
        scientists = [scientist.to_dict(rules=("-missions", )) for scientist in Scientist.query.all()]
        # Return the list of scientists as a response with HTTP status code 200 (OK).
        return make_response(scientists, 200)

    def post(self):
        # Try to create a new scientist from JSON data in the request.
        try:
            new_scientist = Scientist(
                name=request.json['name'],
                field_of_study=request.json['field_of_study']
            )
            # Add the new scientist to the database and commit the transaction.
            db.session.add(new_scientist)
            db.session.commit()
            # Return the newly created scientist as a response with HTTP status code 200 (OK).
            return make_response(new_scientist.to_dict(rules=("-missions", )), 200)
        except ValueError:
            # Handle validation errors by returning an error response with HTTP status code 400 (Bad Request).
            return make_response({"errors": ["validation errors"]}, 400)

# Add the Scientists resource to the Flask API at the route '/scientists'.
api.add_resource(Scientists, "/scientists")

# Define a Flask resource for handling requests related to a specific scientist by their 'id'.
class ScientistsById(Resource):
    def get(self, id):
        # Retrieve a scientist by their 'id' from the database.
        scientist = Scientist.query.filter_by(id=id).one_or_none()
        if scientist is None:
            # If the scientist is not found, return an error response with HTTP status code 404 (Not Found).
            return make_response({"error": "Scientist not found"}, 404)
        # Return the scientist as a response with HTTP status code 200 (OK).
        return make_response(scientist.to_dict(), 200)

    def patch(self, id):
        # Retrieve a scientist by their 'id' from the database.
        scientist = Scientist.query.filter_by(id=id).one_or_none()
        if scientist is None:
            # If the scientist is not found, return an error response with HTTP status code 404 (Not Found).
            return make_response({ "error": "Scientist not found"}, 404)
        
        try:
            # Update the scientist's properties based on JSON data in the request.
            setattr(scientist, "name", request.json['name'])
            setattr(scientist, "field_of_study", request.json['field_of_study'])
            # Add the updated scientist to the database and commit the transaction.
            db.session.add(scientist)
            db.session.commit()
            # Return the updated scientist as a response with HTTP status code 202 (Accepted).
            return make_response(scientist.to_dict(rules=("-planets", "-missions", )), 202)
        except ValueError:
            # Handle validation errors by returning an error response with HTTP status code 400 (Bad Request).
            return make_response({"errors": ["validation errors"]}, 400)
        
    def delete(self, id):
        # Retrieve a scientist by their 'id' from the database.
        scientist = Scientist.query.filter_by(id=id).one_or_none()
        if scientist is None:
            # If the scientist is not found, return an error response with HTTP status code 404 (Not Found).
            return make_response({ "error": "Scientist not found"}, 404)
        # Delete the scientist from the database and commit the transaction.
        db.session.delete(scientist)
        db.session.commit()
        # Return an empty response with HTTP status code 204 (No Content) to indicate successful deletion.

# Add the ScientistsById resource to the Flask API at the route '/scientists/<int:id>' where 'id' is a dynamic parameter.

# Define a Flask resource for handling requests related to planets.
class Planets(Resource):
    def get(self):
        # Retrieve a list of planets from the database and apply serialization rules.
        planets = [planet.to_dict(rules=("-missions", )) for planet in Planet.query.all()]
        # Return the list of planets as a response with HTTP status code 200 (OK).
        return make_response(planets, 200)

# Add the Planets resource to the Flask API at the route '/planets'.

# Define a Flask resource for handling requests related to missions.
class Missions(Resource):
    def post(self):
        try:
            # Try to create a new mission from JSON data in the request.
            new_mission = Mission(
                name=request.get_json()['name'],
                scientist_id=request.get_json()['scientist_id'],
                planet_id=request.get_json()['planet_id']
            )
            # Add the new mission to the database and commit the transaction.
            db.session.add(new_mission)
            db.session.commit()
            # Return the newly created mission as a response with HTTP status code 201 (Created).
            return make_response(new_mission.to_dict(), 201)
        except ValueError:
            # Handle validation errors by returning an error response with HTTP status code 400 (Bad Request).
            return make_response({"errors": ["validation errors"]}, 400)

# Add the Missions resource to the Flask API at the route '/missions'.

# Start the Flask application if this script is the main entry point.
if __name__ == '__main__':
    app.run(port=5555, debug=True)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
