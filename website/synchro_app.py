from website import unsyncro_app
from flask_socketio import SocketIO, emit
from flask_login import current_user
from .db_app import db
from .models import Message


def return_server():
    """
    Passing Flask app to SocketIO Server to run it when called in main.py
    listening channels "ask_email" and "client_send_msg" to get informations from client
    side and send them feedback:
    send_email -> show them which email they have when they are logged it.
    handle_message -> add client chat message to DB and broadcast it to everyone
    :return: socketio server, flask app
    """
    app = unsyncro_app.create_app()
    socketio = SocketIO(app)

    @socketio.on('ask_email')
    def send_email() -> None:
        """Sending email of client to itself back."""
        print(current_user.email)
        emit('get_email',  current_user.email)

    @socketio.on('client_send_msg')
    def handle_message(msg: str) -> None:
        """
        When gets message from client, add it to DB and then share it to everyone
        who is connected as a client, to make no refresh needed website /chat
        On load of this page get data directly from DB, but later after
        load, every messages will be broadcasted by this funciton
        Also check if len of msg > 0, because I don't care about "spam".
        Send data as Python dict which is an object in JS, and can be
        used nearly in same way.
        :param msg: Message that comes from JS client Socket server
        :return: -Null-
        """
        print(msg, current_user)
        if len(msg) > 0:
            new_message = Message(data=msg, id_user=current_user.id)
            db.session.add(new_message)
            db.session.commit()
        show_last_post = db.session.execute("""SELECT User.email as email, User.nick as nick, 
                                             Message.data as data, Message.date as date 
                                             FROM User, Message 
                                             WHERE User.id = Message.id_user 
                                             ORDER BY Message.id desc LIMIT 1
                                            """).first()
        s = show_last_post
        msg_dict = {"email": s.email, "nick": s.nick, "data": s.data, "date": s.date}
        emit('recive_message', msg_dict, broadcast=True)

    return socketio, app
