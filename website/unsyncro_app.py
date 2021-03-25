from . import db_app, config
from flask import Flask
from flask_login import LoginManager


def create_app():
    """
    Making singletons of Flask and SQLAlchemy DB...
    Making 1st config of them.
    Inform Flask app about webpages blueprints and thier paths.
    Then making filer + get use of LoginManager.
    :return: Flask app with configured DB, Secret Key, Login Manager and filter for Notes` deltatime
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = config.Config.SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_app.DB_NAME}'
    app.config['TESTING'] = config.Config.TESTING
    db_app.init_app(app)

    """
    geting access to route and tamplates to show from subfiles
    """
    from .views import views
    from .auth import auth
    from .unauth import unauth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(unauth, url_prefix='/')

    db_app.create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'unauth.login'
    login_manager.init_app(app)

    import datetime as dt

    @app.template_filter()
    def deltatime(value):
        """
        This filter is to make delta time when get saved time and "now" time
        and show it at client side.
        When there is hour/min/sec with "0" at beggining -> remove "0".
        When there is over 1 min -> secounds are not shown.
        When there is over 1 hour -> minutes are not shown.
        :param value: time from database
        :return: refactored delta time
        """
        when_is_now = dt.datetime.utcnow()  # getting "now" server time
        calculations = when_is_now - value  # calculating delta time between now and DB saved info.
        str_calc = str(calculations)
        refactored = str_calc.split(':')  # make list from "date" to make easier refactoring
        if len(refactored) == 3:
            if refactored[-3] == '0':  # when there is less than 60 min -> hour
                refactored[-3] = ''  # when == 0 -> hide
                if refactored[-2] == '00':  # when there is less than 60 sec -> minute
                    refactored[-2] = ''  # when == 0 -> hide
                    refactored = [refactored[-1][0:2] + ' sec']
                    if refactored[0][0] == '0':  # where there is "0" at beggining, remove it.
                        refactored[0] = refactored[0][1:]
                else:
                    refactored = [refactored[-2] + ' min']
                    if refactored[0][0] == '0':  # where there is "0" at beggining, remove it.
                        refactored[0] = refactored[0][1:]
            else:
                refactored = [refactored[-3] + ' hour']
        output = ' '.join(refactored)  # ready to send output
        return output

    @login_manager.user_loader
    def load_user(user_id):
        """
        With Login Manager get ID of current user(client) logged
        :param user_id: info about current user
        :return: SQL query that make int ID of current user
        """
        from .models import User
        return User.query.get(int(user_id))

    return app
