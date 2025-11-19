from flask import flash, redirect
from flask import url_for


class CommentHelper:
    @staticmethod
    def create_comment_validation(comment_text):
        if not comment_text:
            flash("Comment cannot be empty.", "warning")
            return redirect(url_for("main.feed"))
