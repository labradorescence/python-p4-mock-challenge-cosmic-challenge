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

class Scientists(Resource):
    def get(self):
        scientists = [scientist.to_dict(rules = ("-missions",)) for scientist in Scientist.query.all()]

        return make_response(scientists, 200)
    
    def post(self):
       #import ipdb; ipdb.set_trace() 
        try:
            new_scientist = Scientist(
                name = request.json['name'],
                field_of_study = request.json['field_of_study']
            )
            db.session.add(new_scientist)
            db.session.commit()

            return make_response(new_scientist.to_dict(rules=("-missions",)), 200)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
        
api.add_resource(Scientists, "/scientists")

class ScientistsById(Resource):
    def get(self, id):
        #import ipdb; ipdb.set_trace()
        scientist = Scientist.query.filter_by(id=id).one_or_none()

        if scientist is None:
            return make_response({"error": "Scientist not found"}, 404)

        return make_response(scientist.to_dict(), 200)
    
    def patch(self, id):
        scientist = Scientist.query.filter_by(id=id).one_or_none()

        if scientist is None:
            return make_response({"error": "Scientist not found"}, 404)
        
        #import ipdb; ipdb.set_trace()
        try:

            setattr(scientist, "name", request.json["name"])
            setattr(scientist, "field_of_study", request.json['field_of_study'])

            db.session.add(scientist)
            db.session.commit()

            return make_response(scientist.to_dict(rules=("-planets", "-missions",)), 202) #make sure to add rules for both planets and missions both 
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
        
    def delete(self, id):

        scientist = Scientist.query.filter_by(id=id).one_or_none()

        if scientist is None:
            return make_response({"error": "Scientist not found"}, 404)
        
        db.session.delete(scientist)
        db.session.commit()

        return make_response({"message": "deleted"}, 204)

api.add_resource(ScientistsById, '/scientists/<int:id>')


class Planets(Resource):
    def get(self):
        planets = [ planet.to_dict(rules=("-missions",)) for planet in Planet.query.all() ]

        return make_response(planets, 200)
api.add_resource(Planets, '/planets')


class Missions(Resource):
    def post(self):
        new_mission = Mission(
            name=request.get_json()["name"],
            scientist_id=request.get_json()["scientist_id"],
            planet_id=request.get_json()["planet_id"])
        db.session.add(new_mission)
        db.session.commit()

        return make_response(new_mission.to_dict(), 200)
api.add_resource(Missions, '/missions')





if __name__ == '__main__':
    app.run(port=5555, debug=True)
