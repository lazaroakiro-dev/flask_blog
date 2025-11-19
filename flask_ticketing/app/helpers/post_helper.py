from flask import flash, redirect
from flask import url_for


class PostHelper:
    @staticmethod
    def New_Post_Validation(title, content):
        if not title or not content:
            flash("Title and content are required", "danger")
            return redirect(url_for("main.create_post"))