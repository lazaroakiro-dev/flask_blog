from flask import Blueprint, render_template
from flask import request, flash
from flask import redirect, url_for
from flask_login import login_required, login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash

from app.services import authenticate_user, validate_registration
from app.services import create_user
from app.services import LoginForm
 

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/login", methods=["GET", "POST"], endpoint="login")
def auth():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        user = authenticate_user(username, password)
        
        if user:
            login_user(user)
            flash("Logged in successfully", "success")
            return redirect(url_for("main.feed"))
        else:
            flash("Invalid username or password", "danger")
            return redirect(url_for("auth.login"))
        
        return redirect(url_for("main.feed"))
    
    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["POST"], endpoint="logout")
def logout():
    logout_user()
    flash ("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        error_msg, category = validate_registration(username, email, password, confirm)
        if error_msg:
            flash(error_msg, category)
            return redirect(url_for("auth.register"))

        create_user(username, email, password)
        flash("Registration successful. You can now log in", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html")