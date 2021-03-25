from website import run_server
from website.config import Config as Cfg
# get Flask app and web Socket lunched
socketio, app = run_server()
if __name__ == '__main__':
    # use env variables from Config class to run server easy to change
    socketio.run(app, debug=Cfg.FLASK_DEBUG, host=Cfg.HOST_SERVER, port=Cfg.SERVER_PORT)
