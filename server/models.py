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
    # Define a SQLAlchemy model for the 'planets' table
    __tablename__ = 'planets'

    # Define columns for the 'planets' table
    id = db.Column(db.Integer, primary_key=True) # Primary key column
    name = db.Column(db.String)  # Planet name column
    distance_from_earth = db.Column(db.Integer) # Distance from Earth column
    nearest_star = db.Column(db.String) # Nearest star column


   # Add relationship with the 'Mission' model, establishing a link between planets and missions
    missions = db.relationship(
        "Mission", #relationship w/intermediary misson model
        back_populates="planet", #link mission and planet
        cascade="all, delete" #the associated mission object is also deleted from the database.
        #configure the model to cascade deletes
    )

    # Add serialization rules
    # Define serialization rules for excluding the 'missions.planet' relationship
    serialize_rules = ("-missions.planet", )
    #exclude the missions.planet relationship to avoid potential circular references and to control the depth of serialization.
    #without this might end up in an infinite loop
    
    def __repr__(self):
        return f'<Planet {self.id}, {self.name} >'     

class Scientist(db.Model, SerializerMixin):
    # Define a SQLAlchemy model for the 'scientists' table
    __tablename__ = 'scientists'

    # Define columns for the 'scientists' table
    id = db.Column(db.Integer, primary_key=True) # Primary key column
    name = db.Column(db.String)  # Scientist name column
    field_of_study = db.Column(db.String) # Field of study column

    # Add relationship with the 'Mission' model, establishing a link between scientists and missions
    missions = db.relationship(
        "Mission", #relationship w/intermediary misson model
        back_populates="scientist", #link mission and the current class, scientist
        cascade="all, delete" #the associated mission object is also deleted from the database.

    )


    # Add serialization rules
    serialize_rules = ("-missions.scientist", )
    #Set serialization rules to limit the recursion depth.

    # Add validation
    @validates("name")
    def validate_name(self, key, name):
        print(":::::::", self, key, name)
        if not name or len(name) < 1:
            raise ValueError("Name Must Exist.")
        return name
    
    @validates("field_of_study")
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study or len(field_of_study) < 1:
            raise ValueError("Field of study must exist.")
        return field_of_study


    def __repr__(self):
        return f'<Scientist {self.id}, {self.name} >'

class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships
    planet_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))

    planet = db.relationship("Planet", back_populates='missions')
    scientist = db.relationship("Scientist", back_populates="missions")

    # Add serialization rules
    serialize_rules = ("-scientist.missions", "-planet.missions", )

    def __repr__(self):
        return f'<Mission {self.id}, {self.name}, {self.planet}, {self.scientist} >'



    # Add validation
    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Name must exist.")
        return name 
    
    @validates("planet_id")
    def validate_planet_id(self, key, planet_id):
        if planet_id is not None:
            return planet_id 
        raise ValueError("planet_id must exist.")
        
    
    @validates("scientist_id")
    def validate_scientist_id(self, key, scientist_id):
        if scientist_id is not None:
            return scientist_id 
        raise ValueError("scientist_id must exist.")
        


# add any models you may need.


# #backref 
# class Planet(db.Model, SerializerMixin):
#     __tablename__ = 'planets'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     distance_from_earth = db.Column(db.Integer)
#     nearest_star = db.Column(db.String)

#     # Add relationship
#     missions = db.relationship(
#         "Mission", backref="planet", cascade="all, delete")

#     # Add serialization rules
#     serialize_rules = ("-missions.planet", )

# class Scientist(db.Model, SerializerMixin):
#     __tablename__ = 'scientists'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     field_of_study = db.Column(db.String)

#     # Add relationship
#     missions = db.relationship(
#         "Mission", backref="scientist", cascade="all, delete")

#     # Add serialization rules
#     serialize_rules = ("-missions.scientist", )

# class Mission(db.Model, SerializerMixin):
#     __tablename__ = 'missions'

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)

#     # Add relationships
#     planet_id = db.Column(db.Integer, db.ForeignKey("planets.id")) 
#     scientist_id = db.Column(db.Integer, db.ForeignKey("scientists.id"))

#     # Add serialization rules
#     serialize_rules = ("-scientist.missions", "-planet.missions", )