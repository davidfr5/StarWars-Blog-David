from extensions import db
from sqlalchemy.orm import relationship # Import relationship for backref clarity
import json # To help with serializing/deserializing properties if needed, though SQLAlchemy usually handles this if using JSON type.

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False) # Changed username to email for typical login
    password = db.Column(db.String(128), nullable=False) # Storing hashed password in a real app
    favorites = db.relationship("Favorite", backref="user", lazy=True) # A user can have many favorites

    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # Do NOT serialize the password
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Corresponds to SWAPI uid
    name = db.Column(db.String(120), nullable=False)
    # Store other properties as JSON text
    properties = db.Column(db.Text, nullable=True) # Using Text to store JSON string

    favorites_link = db.relationship("Favorite", backref="people", lazy=True, primaryjoin="People.id==Favorite.people_id") # Link for favorites

    def __repr__(self):
        return f'<People {self.name}>'

    def serialize(self):
        props = json.loads(self.properties) if self.properties else {}
        return {
            "id": self.id,
            "name": self.name,
            "properties": props
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True) # Corresponds to SWAPI uid
    name = db.Column(db.String(120), nullable=False)
    # Store other properties as JSON text
    properties = db.Column(db.Text, nullable=True) # Using Text to store JSON string

    favorites_link = db.relationship("Favorite", backref="planet", lazy=True, primaryjoin="Planet.id==Favorite.planet_id") # Link for favorites

    def __repr__(self):
        return f'<Planet {self.name}>'

    def serialize(self):
        props = json.loads(self.properties) if self.properties else {}
        return {
            "id": self.id,
            "name": self.name,
            "properties": props
        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=True)
    # Add a type field to explicitly store if it's 'people' or 'planet' for easier querying/serialization
    item_type = db.Column(db.String(10), nullable=False) # 'people' or 'planet'

    def __repr__(self):
        if self.people_id:
            return f'<Favorite User:{self.user_id} People:{self.people_id}>'
        elif self.planet_id:
            return f'<Favorite User:{self.user_id} Planet:{self.planet_id}>'
        return f'<Favorite User:{self.user_id}>'

    def serialize(self):
        # We need to fetch the actual item details based on its type
        item_name = None
        item_uid = None # Corresponding to the frontend's uid
        if self.item_type == 'people' and self.people: # self.people comes from the backref
            item_name = self.people.name
            item_uid = self.people.id
        elif self.item_type == 'planet' and self.planet: # self.planet comes from the backref
            item_name = self.planet.name
            item_uid = self.planet.id

        return {
            "id": self.id,
            "user_id": self.user_id,
            "item_type": self.item_type,
            "item_id": self.people_id if self.people_id else self.planet_id, # Our internal DB id
            "name": item_name,
            "uid": item_uid # This is what the frontend expects as 'uid'
        }