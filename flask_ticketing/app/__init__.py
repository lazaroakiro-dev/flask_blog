from flask import Flask

from .extensions import blog_db, login_manager
from . extensions import migrate
from .main.routes import main_bp
from .about.routes import about_bp
from .contact.routes import contact_bp
from .auth.routes import auth_bp
from .errors.errors import errors_bp
from app.auth import init_auth


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.DevConfig")
    
    blog_db.init_app(app)
    init_auth(app)  # Login manager initialization
    migrate.init_app(app)
    
    app.register_blueprint(main_bp)
    app.register_blueprint(about_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(errors_bp)
    
    return app