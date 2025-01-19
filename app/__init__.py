from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config  # Import your Config class
import os

from flask import Flask

db = SQLAlchemy()
migrate = Migrate()



# Flask app factory
def create_app():
    app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER)

    app.config.from_object(Config)
    app.secret_key = os.urandom(24)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Register routes
    from app.routes.register_routes import register_routes
    register_routes(app)

    # Debugging message
    print(f"Creating Flask app: {app.name}")

    

    
    
    return app





if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
