from . import synchro_app


def run_server():
    """Starting Socket IO server with DB server and Flask app"""
    return synchro_app.return_server()
