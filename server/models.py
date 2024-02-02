from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship("Mission", #relationship w/intermediary mission model
                               backref="planet", #link mission and planet 
                               cascade="all, delete" #delete all the associated mission obj
                               )

    # Add serialization rules
    serialize_rules = ("-missions.planet", )

    def __repr__(self):
        return f'<Planet {self.id}, {self.name}>'


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    #relationship between the scientist and missions
    missions = db.relationship(
                                "Mission",
                                backref="scientist",
                                cascade="all, delete-orphan"
                            )

    # Add serialization rules
    serialize_rules = ("-missions.scientist", )

    # Add validation
    @validates("name", "field_of_study") # decorator, takes in ("column name") to validate 
    def validate_scientist(self, key, value): 
        print("##########", self, key, value)
        if not value:
            raise ValueError("Value MUST EXIST!!!!!")
        return value
    



    def __resp__(self):
        return f'<Scientist {self.id}, {self.name}>'


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))

    # scientist = db.relationship("Scientist", back_populates="missions")
    # planet = db.relationship("Planet", back_populates="missions")

    # Add serialization rules
    serialize_rules = ("-scientist.missions", "-planet.missions", )

    # Add validation
    # @validates("name", "scientist_id", "planet_id")
    # def validate_input(self, key, value):
    #     if not value:
    #         raise ValueError("ERROR! name, scientist id or planet id must exist ")
    #     return 

    @validates("name")
    def validate_input(self, key, value):
        if not value:
            raise ValueError("ERROR! name")
        return value

    @validates("planet_id")
    def validate_input(self, key, planet_id):
        if planet_id is not None: #if there is a planet id
            return planet_id 
        raise ValueError("planet id is needed")
    
    @validates("scientist_id")
    def validate_input(self, key, scientist_id):
        if scientist_id is not None: #if there is a scientist id
            return scientist_id 
        raise ValueError("scientist id is needed")

    def __repr__(self):
        return f'<Mission {self.id}, {self.name}, {self.planet}, {self.scientist}>'


# add any models you may need.
