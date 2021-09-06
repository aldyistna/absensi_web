from flask import render_template, make_response, flash, redirect, url_for
from flask_restful import Resource, reqparse
from flask_login import login_user

from absensi.model.model import Karyawan
from app import db

parser = reqparse.RequestParser()
parser.add_argument('nik', required=True, help='nik parameter is required')
parser.add_argument('name', required=True, help='nik parameter is required')
parser.add_argument('jabatan', required=True, help='nik parameter is required')
parser.add_argument('username', required=True, help='nik parameter is required')
parser.add_argument('password', required=True, help='password parameter is required')


class KaryawanResource(Resource):
    decorators = []

    def post(self):
        data = parser.parse_args()
        print(data)

        nik_check = Karyawan.query.filter_by(nik=data['nik']).first()
        if nik_check:
            flash('NIK sudah digunakan !')
            return redirect(url_for('add_karyawan'))

        uname_check = Karyawan.query.filter_by(username=data['username']).first()
        if uname_check:
            flash('Username sudah digunakan !')
            return redirect(url_for('add_karyawan'))

        karyawan = Karyawan()

        karyawan.nik = data['nik']
        karyawan.name = data['name']
        karyawan.jabatan = data['jabatan']
        karyawan.username = data['username']
        karyawan.password = data['password']
        karyawan.login = "MOBILE"

        db.session.add(karyawan)
        db.session.commit()
        return redirect(url_for('absen'))
