from flask import render_template, make_response, flash, redirect, url_for
from flask_restful import Resource, reqparse
from flask_login import login_user

from absensi.model.model import Karyawan, KaryawanSchema

parser = reqparse.RequestParser()
parser.add_argument('nik', required=True, help='nik parameter is required')
parser.add_argument('password', required=True, help='password parameter is required')
parser.add_argument('login', required=True, help='password parameter is required')


class LoginResource(Resource):
    decorators = []

    def post(self):
        data = parser.parse_args()

        nik = data['nik']
        password = data['password']
        login = data['login']

        if isinstance(nik, int):
            karyawan = Karyawan.query.filter(Karyawan.nik == nik) \
                .filter(Karyawan.password == password) \
                .filter(Karyawan.login == login).first()
        else:
            karyawan = Karyawan.query.filter(Karyawan.username == nik) \
                .filter(Karyawan.password == password) \
                .filter(Karyawan.login == login).first()

        karyawan_schema = KaryawanSchema()
        output = karyawan_schema.dump(karyawan).data
        if output:
            if login == 'WEB':
                login_user(karyawan, remember=True)
                return redirect(url_for('absen'))
            return {
                'status': 1,
                'message': 'success',
                'data': output
            }
        else:
            if login == 'WEB':
                flash('Username atau password salah !')
                return redirect(url_for('loginresource'))
            return {
                'status': 0,
                'message': 'failed',
                'data': ''
            }

    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('login.html'), 200, headers)
