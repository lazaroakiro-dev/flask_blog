from werkzeug.security import check_password_hash

from app.models import User
from app.extensions import blog_db
from app.helpers import hash_password


def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


def validate_registration(username, email, password, confirm):
    if not username or not email or not password:
        return "All fields are required", "danger"
    if password != confirm:
        return "Passwords do not match", "danger"
    if User.query.filter_by(username=username).first():
        return "Username already taken", "warning"
    if User.query.filter_by(email=email).first():
        return "Email already registered", "warning"
    return None, None


def create_user(username, email, password):
    new_user = User(
        username=username,
        email=email,
        password_hash=hash_password(password)
    )
    blog_db.session.add(new_user)
    blog_db.session.commit()
    return new_user