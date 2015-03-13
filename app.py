from flask.ext.mongoengine import MongoEngine
from flask import Flask


app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB':'mydatabase'}


db = MongoEngine(app)

def register_blueprints(app):
    from views import nextbus
    app.register_blueprint(nextbus)

register_blueprints(app)

if __name__ == '__main__':
    app.run()
