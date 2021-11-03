from flask import Flask,session
from .config import Config,configdb
from .connection.models.connectionDb import ConnectionRedis
from .connection import connection
from flask import _app_ctx_stack


from flask_bootstrap import Bootstrap

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(connection)
    bootstrap=Bootstrap(app)
    context = _app_ctx_stack
    if not hasattr(context, 'db'):
        context.db = ConnectionRedis(**configdb)
    return app