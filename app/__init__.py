from flask import Flask
from flask_mongoengine import MongoEngine
from flask.json import JSONEncoder as BaseJSONEncoder
import datetime

db = MongoEngine()

class JSONEncoder(BaseJSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(JSONEncoder, self).default(obj)

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    app.json_encoder = JSONEncoder

    db.init_app(app)

    with app.app_context():
        from . import routes

    return app
