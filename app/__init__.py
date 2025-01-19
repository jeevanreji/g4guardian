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
    app = Flask(__name__, template_folder='/Users/jeevanreji/Documents/segMaster/templates/',static_folder='/Users/jeevanreji/Documents/segMaster/static')

    # Configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'mysql+pymysql://admin:Realmadrid123@database-1-instance-1.cxq6e0c880zp.us-east-1.rds.amazonaws.com:3306/database-1'
    )  # Update your DB URI here
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TEMPLATES_AUTO_RELOAD'] = True
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
