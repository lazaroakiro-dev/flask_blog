from flask_login import current_user
from flask import flash, redirect
from flask import url_for

from app.models import Comment
from app.extensions import blog_db


class CommentService:
    @staticmethod
    def create_new_comment(comment_text, post_id):
        if comment_text == "": pass
        else:
            comment = Comment(content=comment_text, user_id=current_user.id, post_id=post_id)
            blog_db.session.add(comment)
            blog_db.session.commit()
    
            flash("Comment added!", "success")

    @staticmethod
    def author_comment_delete(comment_id):
        comment = Comment.query.get_or_404(comment_id)
    
        # Only allow the author to delete
        if comment.user.id != current_user.id:
            flash("You cannot delete this comment.", "danger")
        
        else:
            blog_db.session.delete(comment)
            blog_db.session.commit()
            flash("Comment deleted successfully.", "success")