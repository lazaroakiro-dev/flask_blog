from flask import Blueprint, render_template
from flask_login import login_required
 

about_bp = Blueprint("about", __name__, template_folder="templates")

@about_bp.route("/about")
@login_required
def about():
	return render_template("about/about.html")
