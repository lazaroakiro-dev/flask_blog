import os


class DevConfig:
    DEBUG = True
    SECRET_KEY = os.environ.get("SECRET_KEY", "fallback-key-for-dev")
    SQLALCHEMY_DATABASE_URI = "sqlite:///blog.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False