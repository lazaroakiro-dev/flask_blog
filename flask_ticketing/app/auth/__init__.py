from app.extensions import login_manager
from .routes import auth_bp
from app.models import User


def init_auth(app):
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))