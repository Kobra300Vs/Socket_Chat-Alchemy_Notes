from flask import Blueprint, render_template
from flask_login import current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    """
    Sending to client root/ main/ welcome page, as U call it.
    :return: main.html for current user even when not logged in
    """
    return render_template("main.html", user=current_user)
