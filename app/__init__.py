from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config  # Import your Config class
import os

from flask import Flask
from flask import Flask
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()

mail = Mail()

# Flask app factory
def create_app():
    app = Flask(__name__, template_folder=Config.TEMPLATE_FOLDER,static_folder=Config.STATIC_FOLDER)


    app.secret_key = os.urandom(24)
    app.config.from_object(Config)
    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    mail.init_app(app)
    # Register routes
    from app.routes.register_routes import register_routes
    register_routes(app)

    # Debugging message
    print(f"Creating Flask app: {app.name}")

    

    
    
    return app





if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
