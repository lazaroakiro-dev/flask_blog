from flask import flash

from app.models import Post
from app.extensions import blog_db
from app.models import Post, Comment


class PostService:
    @staticmethod
    def create_post(title, content, author):
        post = Post(title=title, content=content, author=author, votes=0)
        blog_db.session.add(post)
        blog_db.session.commit()
        flash("Post created successfully", "success")
        return post
    
    @staticmethod
    def feed_creation():
        posts = Post.query.order_by(Post.votes.desc(), Post.created_at.desc()).all()
        feed = []
        for post in posts:
            top_comment = Comment.query.filter_by(post_id=post.id)\
                .order_by(Comment.votes.desc())\
                .first()
            other_comments = Comment.query.filter_by(post_id=post.id)\
                .order_by(Comment.votes.desc())\
                .all()[1:]
            feed.append({
                "post": post,
                "top_comment": top_comment,
                "other_comments": other_comments
            })
        return feed
