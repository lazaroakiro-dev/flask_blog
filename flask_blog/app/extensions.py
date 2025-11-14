from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


login_manager = LoginManager()


blog_db = SQLAlchemy()


migrate = Migrate()