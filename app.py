from flask.ext.mongoengine import MongoEngine
from flask import Flask

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {'DB':'mydatabase'}

db = MongoEngine(app)

if __name__ == '__main__':
    app.run()
