import logging

from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from flask_marshmallow import Marshmallow
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from flask import request
from flask import jsonify

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage, exceptions

import settings
UPLOAD_FOLDER = 'static/uploaded/'
PICTURE_FOLDER = 'static/picture/'
app = Flask(__name__, static_url_path="", static_folder='static')
cors = CORS(app, resources={r"/kkp/*": {"origins": "*"}})


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS
app.config["JSON_SORT_KEYS"] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PICTURE_FOLDER'] = PICTURE_FOLDER

db = SQLAlchemy(app)
db.reflect()
ma = Marshmallow(app)

api = Api(app)
api.prefix = '/ta'

cred = credentials.Certificate(app.root_path + "/credential.json")
bucket = firebase_admin.initialize_app(cred, {
    'storageBucket': 'project-ta-7310e.appspot.com',
}, name='storage')
bucket_app = storage.bucket(app=bucket)


from absensi.router import *


@app.route('/')
def hello_world():
    app.logger.debug('Recommendation API is up')
    app.logger.info('Info')
    return jsonify(api='Recommendation API',
                   ver=1.0)


@app.route('/ta/')
def ta_test():
    app.logger.debug('Recommendation API is up')
    app.logger.info('Info')
    return jsonify(api='Recommendation API',
                   ver=1.0)


@app.route('/get-ip')
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


if __name__ == '__main__':
    handler = RotatingFileHandler('kkp.log', maxBytes=100000000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(use_reloader=False)
