import os
import requests
import json
from app import create_app
from extensions import db
from models import User, People, Planet #, Favorite (not seeding favorites directly)

# Load environment variables (optional, if your DB URL is in .env)
from dotenv import load_dotenv
load_dotenv()

def fetch_swapi_data(endpoint):
    """Fetches data from SWAPI.tech with pagination."""
    all_results = []
    url = f"https://www.swapi.tech/api/{endpoint}"
    print(f"Fetching {endpoint} data from SWAPI...")
    while url:
        response = requests.get(url)
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        # SWAPI.tech has 'results' for list and 'result' for detail
        if 'results' in data and data['results']:
            for item in data['results']:
                # Fetch detailed info for each item
                detail_url = item['url']
                detail_response = requests.get(detail_url)
                detail_response.raise_for_status()
                detail_data = detail_response.json()
                if 'result' in detail_data and 'properties' in detail_data['result']:
                    # Add uid to properties for consistency
                    props = detail_data['result']['properties']
                    props['uid'] = detail_data['result']['uid'] 
                    all_results.append({
                        'uid': detail_data['result']['uid'],
                        'name': detail_data['result']['properties']['name'],
                        'properties': props # Store all properties
                    })
        
        url = data.get('next') # Get next page URL
    print(f"Finished fetching {len(all_results)} {endpoint}.")
    return all_results

def seed_database():
    app = create_app()
    with app.app_context():
        print("Clearing existing data...")
        db.drop_all() # Drop all tables
        db.create_all() # Recreate all tables

        print("Seeding database...")

        # Create a default user
        print("Creating default user...")
        # In a real app, hash the password!
        user = User(email="test@example.com", password="password123") 
        db.session.add(user)
        db.session.commit()
        print(f"User created: {user.email} (ID: {user.id})")

        # Seed People
        people_data = fetch_swapi_data("people")
        for p_data in people_data:
            # We use SWAPI's uid as our id for easier mapping with frontend and URLs
            person = People(id=int(p_data['uid']), name=p_data['name'], properties=json.dumps(p_data['properties']))
            db.session.add(person)
        db.session.commit()
        print(f"Seeded {len(people_data)} people.")

        # Seed Planets
        planets_data = fetch_swapi_data("planets")
        for p_data in planets_data:
            # We use SWAPI's uid as our id for easier mapping with frontend and URLs
            planet = Planet(id=int(p_data['uid']), name=p_data['name'], properties=json.dumps(p_data['properties']))
            db.session.add(planet)
        db.session.commit()
        print(f"Seeded {len(planets_data)} planets.")

        print("Database seeding complete!")

if __name__ == "__main__":
    seed_database()