import logging

from flask import Flask, redirect, url_for
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
from flask_marshmallow import Marshmallow
from logging.handlers import RotatingFileHandler
from flask_cors import CORS
from flask import request
from flask import jsonify
from flask_login import LoginManager, UserMixin

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

# from absensi.model.model import Karyawan

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
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

db = SQLAlchemy(app)
db.reflect()
ma = Marshmallow(app)

api = Api(app)
api.prefix = ''

cred = credentials.Certificate(app.root_path + "/credential.json")
bucket = firebase_admin.initialize_app(cred, {
    'storageBucket': 'absensi-2b565.appspot.com',
}, name='storage')
bucket_app = storage.bucket(app=bucket)

login_manager = LoginManager()
login_manager.login_view = 'loginresource'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in the query for the user
    return Karyawan.query.get(int(user_id))

# blueprint for auth routes in our app
from absensi.router.auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from absensi.router.route import main as main_blueprint
app.register_blueprint(main_blueprint)
from absensi.router import *


@app.route('/')
def hello_world():
    app.logger.debug('Recommendation API is up')
    app.logger.info('Info')
    return redirect(url_for('absen'))


@app.route('/get-ip')
def get_my_ip():
    return jsonify({'ip': request.remote_addr}), 200


if __name__ == '__main__':
    handler = RotatingFileHandler('absen.log', maxBytes=100000000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(use_reloader=False)


class Karyawan(UserMixin, db.Model):
    __tabelname__ = 'karyawan'
    __table_args__ = {'extend_existing': True}
    # absen = db.relationship("Absen", uselist=False, back_populates="karyawan")


class Absen(db.Model):
    __tabelname__ = 'absen'
    __table_args__ = {'extend_existing': True}
    # nik = db.column(db.Integer, db.ForeignKey("karyawan.nik"))
    # karyawan = db.relationship("Karyawan", back_populates="absen")


class KaryawanSchema(ma.ModelSchema):
    class Meta:
        model = Karyawan


class AbsenSchema(ma.ModelSchema):
    # karyawan = ma.Nested(KaryawanSchema, many=False)

    class Meta:
        model = Absen
