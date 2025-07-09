from flask import Blueprint, jsonify, request
from extensions import db
from models import User, People, Planet, Favorite
import json # For loading JSON properties

api = Blueprint("api", __name__) # Corrected: only one definition

# Simulación de usuario activo (en un entorno real, esto vendría de la autenticación)
# Para este ejercicio, asumiremos que siempre hay un usuario con ID 1
CURRENT_USER_ID = 1

# --- Endpoints para People ---
@api.route("/people", methods=["GET"])
def get_people():
    people = People.query.all()
    # Serialize each person, including their properties
    return jsonify([p.serialize() for p in people]), 200

@api.route("/people/<int:people_id>", methods=["GET"])
def get_person(people_id):
    person = People.query.get(people_id) # Use get instead of get_or_404 initially
    if person is None:
        return jsonify({"msg": "Person not found"}), 404
    return jsonify(person.serialize()), 200

# --- Endpoints para Planets ---
@api.route("/planets", methods=["GET"])
def get_planets():
    planets = Planet.query.all()
    # Serialize each planet, including their properties
    return jsonify([p.serialize() for p in planets]), 200

@api.route("/planets/<int:planet_id>", methods=["GET"])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id) # Use get instead of get_or_404 initially
    if planet is None:
        return jsonify({"msg": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# --- Endpoints para Users ---
@api.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.serialize() for u in users]), 200

@api.route("/users/favorites", methods=["GET"])
def get_user_favorites():
    # Fetch favorites for the CURRENT_USER_ID
    favorites = Favorite.query.filter_by(user_id=CURRENT_USER_ID).all()
    
    # Serialize each favorite, ensuring it matches the frontend's expected structure
    # (e.g., {'name': 'Luke Skywalker', 'uid': '1', 'type': 'people'})
    serialized_favorites = []
    for fav in favorites:
        serialized_favorites.append(fav.serialize()) # Use the serialize method from Favorite model

    return jsonify(serialized_favorites), 200

# --- Endpoints para Favorite (POST) ---
@api.route("/favorite/people/<int:people_id>", methods=["POST"])
def add_people_favorite(people_id):
    # Check if the person exists in our DB
    person = People.query.get(people_id)
    if not person:
        return jsonify({"msg": "Person not found in database"}), 404
    
    # Check if already a favorite for this user
    existing_fav = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID, 
        people_id=people_id, 
        item_type='people'
    ).first()
    if existing_fav:
        return jsonify({"msg": "Person is already a favorite"}), 409 # Conflict

    fav = Favorite(user_id=CURRENT_USER_ID, people_id=people_id, item_type='people')
    try:
        db.session.add(fav)
        db.session.commit()
        return jsonify({"message": f"Person '{person.name}' added to favorites"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding favorite", "error": str(e)}), 500

@api.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planet_favorite(planet_id):
    # Check if the planet exists in our DB
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"msg": "Planet not found in database"}), 404

    # Check if already a favorite for this user
    existing_fav = Favorite.query.filter_by(
        user_id=CURRENT_USER_ID, 
        planet_id=planet_id, 
        item_type='planet'
    ).first()
    if existing_fav:
        return jsonify({"msg": "Planet is already a favorite"}), 409 # Conflict

    fav = Favorite(user_id=CURRENT_USER_ID, planet_id=planet_id, item_type='planet')
    try:
        db.session.add(fav)
        db.session.commit()
        return jsonify({"message": f"Planet '{planet.name}' added to favorites"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding favorite", "error": str(e)}), 500

# --- Endpoints para Favorite (DELETE) ---
@api.route("/favorite/people/<int:people_id>", methods=["DELETE"])
def delete_people_favorite(people_id):
    fav = Favorite.query.filter_by(user_id=CURRENT_USER_ID, people_id=people_id, item_type='people').first()
    if not fav:
        return jsonify({"msg": "Favorite person not found for this user"}), 404
    try:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"message": "Favorite person removed"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error removing favorite", "error": str(e)}), 500

@api.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet_favorite(planet_id):
    fav = Favorite.query.filter_by(user_id=CURRENT_USER_ID, planet_id=planet_id, item_type='planet').first()
    if not fav:
        return jsonify({"msg": "Favorite planet not found for this user"}), 404
    try:
        db.session.delete(fav)
        db.session.commit()
        return jsonify({"message": "Favorite planet removed"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error removing favorite", "error": str(e)}), 500