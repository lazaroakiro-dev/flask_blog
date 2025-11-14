from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash

from app.extensions import blog_db


class User(blog_db.Model, UserMixin):
    __tablename__ = "user"
    
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    username = blog_db.Column(blog_db.String(80), unique=True, nullable=False)
    email = blog_db.Column(blog_db.String(120), unique=True, nullable=False)
    password_hash = blog_db.Column(blog_db.String(128), nullable=False)
    
    votes = blog_db.relationship("Vote", backref="user", lazy=True)
    
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
    
    # Relationship to comments
    comments = blog_db.relationship("Comment", backref="post", lazy="dynamic")
    
    votes_rel = blog_db.relationship("Vote", backref="post", lazy=True)
    

class Comment(blog_db.Model):
    __tablename__ = "Comments"
    
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    post_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("posts.id"), nullable=False)
    author = blog_db.Column(blog_db.String(50), nullable=False)
    content = blog_db.Column(blog_db.Text, nullable=False)
    created_at = blog_db.Column(blog_db.DateTime, default=datetime.utcnow)
    votes = blog_db.Column(blog_db.Integer, default=0)
    
    # Nested Replies
    parent_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("Comments.id"), nullable=True)
    replies = blog_db.relationship(
        "Comment",
        backref=blog_db.backref("parent", remote_side=[id]),
        lazy="dynamic"
    )
    
    
class Vote(blog_db.Model):
    __tablename__ = "votes"
    
    id = blog_db.Column(blog_db.Integer, primary_key=True)
    user_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("user.id"), nullable=False)
    post_id = blog_db.Column(blog_db.Integer, blog_db.ForeignKey("posts.id"), nullable=False)
    value = blog_db.Column(blog_db.Integer, nullable=False)
    
    # Prevent duplicate votes per user/post
    __table_args__ = (
        blog_db.UniqueConstraint("user_id", "post_id", name="unique_user_post_vote"),
        )