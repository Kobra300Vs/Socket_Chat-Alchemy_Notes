from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import Note, User  # , Message
from .db_app import db
from flask_login import login_required, logout_user, current_user
import json

auth = Blueprint('auth', __name__)


@auth.route('/logout')
@login_required
def logout() -> redirect:
    """ONLY when logged... This function logout current user and redirect to /login"""
    logout_user()
    return redirect(url_for('unauth.login'))


@auth.route('/notes', methods=['GET', 'POST'])
@login_required
def notes() -> render_template():
    """
    ONLY when logged
    Allow adding notes to DB and show them at /notes
    if want to remove any, U have index.js funcion removeNote(id_of_note)
    which call function .auth.delete_note()
    :return: notes.html for current user
    """
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) > 0:
            flash('Note added.', category='succes')
            new_note = Note(data=note, id_user=current_user.id)
            db.session.add(new_note)
            db.session.commit()
        else:
            flash('There is no note to save.', category='note_len_short')
    return render_template("notes.html", user=current_user)


@auth.route('/delete-note', methods=['POST'])
@login_required
def delete_note() -> json:
    """ONLY when logged... This function is to remove note from DB when someone click X button"""
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.id_user == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})


@auth.route('/chat', methods=['GET', 'POST'])
@login_required
def chat() -> render_template:
    """
    ONLY when logged
    This page NOT need to be refreshed!
    When user join /chat it will get all messages from DB and then
    all the magic is done by JS and Flask SocketIO communication
    Only at load it work with DB to get data and Jinja work with them.
    :return: chat.html
    """
    # if request.method == 'POST':
    #     message = request.form.get('message')
    #     if len(message) > 0:
    #         new_message = Message(data=message, id_user=current_user.id)
    #         db.session.add(new_message)
    #         db.session.commit()
    #     else:
    #         flash('You cannot post empty message.', category='note_len_short')
    # # show_all_posts = Note.query.filter(Note.data.endswith("s")).order_by(Note.data).all()
    show_all_posts = db.session.execute('SELECT User.email as email, User.nick as nick,'
                                        ' Message.data as data, Message.date as date'
                                        ' FROM User, Message'
                                        ' WHERE User.id = Message.id_user')
    return render_template("chat.html", user=current_user, messages=show_all_posts)


@auth.route('/profile/<target_email>', methods=['GET', 'POST'])
@login_required
def profile(target_email: str) -> render_template:
    """
    ONLY when logged
    Show target user (by email) page. There are its all
    messages that it post at /chat
    :param target_email: Email of target user, that will be shown as its /profile/target_email
    :return: Default profile.html, but with data about target email chat msgs.
    """
    target = User.query.filter_by(email=target_email).first()
    return render_template("profile.html", user=current_user, target=target)
