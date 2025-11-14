from app.models import Post
from app.extensions import blog_db


class PostService:
    @staticmethod
    def create_post(title, content, author):
        post = Post(title=title, content=content, author=author, votes=0)
        blog_db.session.add(post)
        blog_db.session.commit()
        return post