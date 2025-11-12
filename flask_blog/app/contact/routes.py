from flask import Blueprint, redirect
from flask import render_template, request
from flask import url_for
from flask_login import login_required

contact_bp = Blueprint("contact", __name__, template_folder="templates")

@contact_bp.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        message = request.form.get("message")
        # Process form data here
        return redirect(url_for("/"))
    return render_template("contact/contact.html")