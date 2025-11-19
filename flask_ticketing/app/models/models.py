from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from app.extensions import blog_db


class User(blog_db.Model, UserMixin):
    __tablename__ = "users"
    
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    username = blog_db.Column(blog_db.String(80), unique=True, nullable=False)
    email = blog_db.Column(blog_db.String(120), unique=True, nullable=False)
    password_hash = blog_db.Column(blog_db.String(128), nullable=False)

    # Relationships
    posts = blog_db.relationship("Post", back_populates="author_rel", lazy="dynamic")
    comments = blog_db.relationship("Comment", back_populates="user", lazy="dynamic")
    votes = blog_db.relationship("Vote", back_populates="user", lazy="dynamic")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


class Post(blog_db.Model):
    __tablename__ = "posts"
    
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    author = blog_db.Column(blog_db.String(50), nullable=False)
    title = blog_db.Column(blog_db.String(200), nullable=False)
    content = blog_db.Column(blog_db.Text, nullable=False)
    created_at = blog_db.Column(blog_db.DateTime, default=datetime.utcnow)
    votes = blog_db.Column(blog_db.Integer, default=0)

    # Foreign key to User (optional if you want to link posts to users)
    author_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("users.id"))

    # Relationships
    author_rel = blog_db.relationship("User", back_populates="posts")
    comments = blog_db.relationship("Comment", back_populates="post", lazy="dynamic")
    votes_rel = blog_db.relationship("Vote", back_populates="post", lazy="dynamic")


class Comment(blog_db.Model):
    __tablename__ = "comments"
    
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    content = blog_db.Column(blog_db.Text, nullable=False)
    created_at = blog_db.Column(blog_db.DateTime, default=datetime.utcnow)
    votes = blog_db.Column(blog_db.Integer, default=0)

    # Foreign keys
    post_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("posts.id"), nullable=False)
    user_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("users.id"), nullable=False)

    # Relationships
    user = blog_db.relationship("User", back_populates="comments")
    post = blog_db.relationship("Post", back_populates="comments")
    parent = blog_db.relationship("Comment", back_populates="replies", remote_side=[id])

    # Nested Replies
    parent_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("comments.id"), nullable=True)
    replies = blog_db.relationship("Comment", back_populates="parent")


class Vote(blog_db.Model):
    __tablename__ = "votes"
    
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    user_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("users.id"), nullable=False)
    post_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("posts.id"), nullable=False)
    value = blog_db.Column(blog_db.Integer, nullable=False)

    # Relationships
    user = blog_db.relationship("User", back_populates="votes")
    post = blog_db.relationship("Post", back_populates="votes_rel")

    # Prevent duplicate votes per user/post
    __table_args__ = (blog_db.UniqueConstraint("user_id", "post_id", name="unique_user_post_vote"),)