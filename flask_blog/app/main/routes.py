from flask import Blueprint, render_template
from flask import request, redirect
from flask import url_for, flash
from flask_login import login_required, current_user

from app.models import Post, Comment
from app.extensions import blog_db
from app.services import PostService, VoteService


main_bp = Blueprint("main", __name__, template_folder="templates")


@main_bp.route("/")
@login_required
def feed():
    posts = Post.query.order_by(Post.votes.desc(), Post.created_at.desc()).all()
    
    feed_data = []
    for post in posts:
        top_comment = Comment.query.filter_by(post_id=post.id)\
            .order_by(Comment.votes.desc())\
            .first()
        other_comments = Comment.query.filter_by(post_id=post.id)\
            .order_by(Comment.votes.desc())\
            .all()[1:]
        feed_data.append({
            "post": post,
            "top_comment": top_comment,
            "other_comments": other_comments
        })
    return render_template("main/feed.html", feed_data=feed_data)


@main_bp.route("/create_post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        
        if not title or not content:
            flash("Title and content are required", "danger")
            return redirect(url_for("main.create_post"))
        
        # Create new post
        new_post = Post(
            title=title,
            content=content,
            author=current_user.username,
            votes=0
        )
        blog_db.session.add(new_post)
        blog_db.session.commit()
        
        flash("Post created successfully", "success")
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
    
    if not comment_text:
        flash("Comment cannot be empty.", "warning")
        return redirect(url_for("main.feed"))
    
    comment = Comment(content=comment_text, user_id=current_user.id, post_id=post_id)
    blog_db.session.add(comment)
    blog_db.session.commit()
    
    flash("Comment added!", "success")
    return redirect(url_for("main.feed"))


@main_bp.route("/comments/<int:comment_id>/delete", methods=["POST"])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    # Only allow the author to delete
    if comment.user.id != current_user.id:
        flash("You cannot delete this comment.", "danger")
        return redirect(url_for("main.feed"))
    
    blog_db.session.delete(comment)
    blog_db.session.commit()
    flash("Comment deleted successfully.", "success")
    return redirect(url_for("main.feed"))