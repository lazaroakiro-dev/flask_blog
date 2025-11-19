from flask import Blueprint, render_template
from flask import request, redirect
from flask import url_for, flash
from flask_login import login_required, current_user

from app.models import Post, Comment
from app.extensions import blog_db
from app.services import PostService, VoteService
from app.helpers import PostHelper, CommentHelper
from app.services import CommentService


main_bp = Blueprint("main", __name__, template_folder="templates")

@main_bp.route("/")
@login_required
def feed():
    feed_data = PostService.feed_creation()
    return render_template("main/feed.html", feed_data=feed_data)


@main_bp.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        PostHelper.New_Post_Validation(title=title, content=content)
        
        PostService.create_post(title=title, content=content, author=current_user.username)
        return redirect(url_for("main.feed"))

    return render_template("main/create_post.html")


@main_bp.route("/post/<int:post_id>/upvote", methods=["POST"])
@login_required
def upvote_post(post_id):
    VoteService.cast_vote(current_user.id, post_id, +1)
    flash("Upvoted!", "success")
    return redirect(url_for("main.feed"))


@main_bp.route("/post/<int:post_id>/downvote", methods=["POST"])
@login_required
def downvote_post(post_id):
    VoteService.cast_vote(current_user.id, post_id, -1)
    flash("Downvoted!", "warning")
    return redirect(url_for("main.feed"))


@main_bp.route("/post/<int:post_id>/comments", methods=["POST"])
@login_required
def add_comment(post_id):
    comment_text = request.form.get("comment", "").strip()
    
    CommentHelper.create_comment_validation(comment_text)
    CommentService.create_new_comment(comment_text, post_id)
    return redirect(url_for("main.feed"))


@main_bp.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    CommentService.author_comment_delete(comment_id=comment_id)
    return redirect(url_for("main.feed"))
