from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app.extensions import blog_db


class User(blog_db.Model, UserMixin):
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    username = blog_db.Column(blog_db.String(80), unique=True, nullable=False)
    email = blog_db.Column(blog_db.String(120), unique=True, nullable=False)
    password_hash = blog_db.Column(blog_db.String(128), nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)