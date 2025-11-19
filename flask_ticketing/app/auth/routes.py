from flask import Blueprint, render_template
from flask import request, flash
from flask import redirect, url_for
from flask_login import login_required, login_user
from flask_login import logout_user
from werkzeug.security import check_password_hash

from app.services import authenticate_user, validate_registration
from app.services import create_user
from app.services import LoginForm, LogoutForm
from app.services import RegisterForm
 

auth_bp = Blueprint("auth", __name__, template_folder="templates")

@auth_bp.route("/login", methods=["GET", "POST"], endpoint="login")
def auth():
    form = LoginForm()
    form_b = LogoutForm()
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
    
    if form_b.validate_on_submit():
        return redirect(url_for("auth.logout"))
    
    return render_template("login.html", form=form, form_b=form_b)


@auth_bp.route("/logout", methods=["POST"], endpoint="logout")
def logout():
    logout_user()
    flash ("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form_register = RegisterForm()
    if form_register.validate_on_submit():
        username = form_register.username.data
        email = form_register.email.data
        password = form_register.password.data
        confirm = form_register.confirm.data

        error_msg, category = validate_registration(username, email, password, confirm)
        if error_msg:
            flash(error_msg, category)
            return redirect(url_for("auth.register"))

        create_user(username, email, password)
        flash("Registration successful. You can now log in", "success")
        return redirect(url_for("auth.login"))
    
    return render_template("register.html", form=form_register)