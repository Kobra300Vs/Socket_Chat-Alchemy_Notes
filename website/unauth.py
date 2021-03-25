from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from .db_app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user
import re

unauth = Blueprint('unauth', __name__)

@unauth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login NOT requied!
    When user click "Login" button, get his data with POST
    and check if it is registred, or if it password is correct
    :return: login.html
    """
    if request.method == 'POST':
        email = request.form.get('email')
        email = email.lower()
        pwd = request.form.get('pwd')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.pwd, pwd):
                flash("Logged in", category='succes')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Bro, wrong password...", category='log_pass')
        else:
            flash("Bro, register right now!", category='log_email')

    return render_template("login.html", user=current_user)


@unauth.route('/registration', methods=['GET', 'POST'])
def register():
    """
    Login NOT requied!
    When user click "Register now!" button, get his data with POST
    and check if it is registred, or if it password is correctly save,
    or email is valid, or nick is at least 3 char long but not longer than 69
    :return: register.html
    """
    if request.method == 'POST':
        email = request.form.get('email')
        nick = request.form.get('nickname')
        pwd_f = request.form.get('password_Fst')
        pwd_c = request.form.get('password_Con')
        user = User.query.filter_by(email=email).first()
        if user:
            flash("This email was already used.", category='reg_same_email')
        elif pwd_f != pwd_c:
            flash("Passwords don't match!", category='reg_pwd_not_eq')
        elif len(nick) < 4 or len(nick) > 70:
            flash("Nickname is not in bounds of <4, 70>.", category='reg_nick_len')
        elif len(email) < 6 or len(email) > 150:
            flash("E-mail something is wrong with lenght of your email.", category='reg_email_len')
        elif len(pwd_f) < 7 or len(pwd_f) > 64:
            flash("For safety check, your password have to be longer"
                  " than 6 charakters, and not longer than 32 charakters", category='reg_pwd_len')
        else:
            new_user = User(email=email, nick=nick, pwd=generate_password_hash(pwd_f, method='sha256'))
            db.session.add(new_user)
            email_pattern = r"^[a-z0-9]([\w\.-]+)@([\w]+)(\.[\w]+)$"
            if re.match(email_pattern, email):
                db.session.commit()
                flash("Account created!", category='succes')
                return redirect(url_for('views.home', user=current_user))
            else:
                db.session.rollback()
                flash("You are not supposed to change HTML!", category='reg_email_validator')
                login_user(new_user, remember=True)

    return render_template("registration.html", user=current_user)
