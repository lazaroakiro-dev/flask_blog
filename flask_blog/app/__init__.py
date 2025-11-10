from flask import Flask

from .main.routes import main_bp
from .about.routes import about_bp
from .contact.routes import contact_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    
    
    app.register_blueprint(main_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)
    
    return app