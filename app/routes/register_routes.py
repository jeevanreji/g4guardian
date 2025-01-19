# app/routes.py

from app.routes.user_routes import user_routes
from app.routes.energy_routes import energy_routes
from app.routes.master_routes import master_routes


def register_routes(app):
    """Register the blueprints to the app"""
    app.register_blueprint(user_routes, url_prefix='/')
    app.register_blueprint(energy_routes, url_prefix='/energy')
    app.register_blueprint(master_routes, url_prefix='/master')
    