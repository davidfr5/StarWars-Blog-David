from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from extensions import db # Import db from extensions
from config import Config # Import Config class

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # Load configuration from Config object

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Import and register blueprints inside create_app to avoid circular imports
    from routes import api
    app.register_blueprint(api, url_prefix='/api') # Added a URL prefix for the API

    # Define a simple root route for testing
    @app.route('/')
    def index():
        return "Welcome to the Star Wars Blog API!"

    return app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        # This will create tables if they don't exist, useful for initial setup
        # For production, use flask db migrate/upgrade
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)