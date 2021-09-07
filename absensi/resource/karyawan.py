from flask import flash, redirect, url_for
from flask_restful import Resource, reqparse
from sqlalchemy import text

from absensi.model.model import Karyawan, KaryawanSchema
from app import db

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, help='nik parameter is required')
parser.add_argument('nik', required=True, help='nik parameter is required')
parser.add_argument('name', required=True, help='nik parameter is required')
parser.add_argument('jabatan', required=True, help='nik parameter is required')
parser.add_argument('username', required=True, help='nik parameter is required')
parser.add_argument('password', required=True, help='password parameter is required')


class KaryawanResource(Resource):
    decorators = []

    def post(self):
        data = parser.parse_args()

        karyawan = Karyawan()

        karyawan.nik = data['nik']
        karyawan.name = data['name']
        karyawan.jabatan = data['jabatan']
        karyawan.username = data['username']
        karyawan.password = data['password']
        karyawan.login = "MOBILE"

        db.session.add(karyawan)

        db.session.commit()
        return redirect(url_for('karyawan'))

    def delete(self, id=None):
        install = Karyawan.query.get(id)

        db.session.delete(install)
        db.session.commit()
        return {
            'data': '',
            'message': 'Success',
            'status': 'Success'
        }


def get_karyawan(request, db, id=None):
    if id:
        kar_schema = KaryawanSchema()
        kar = Karyawan.query.filter_by(id=id, login='MOBILE').first()
        return kar_schema.dump(kar).data

    filter_where = request.args.get('filter')
    where = ''
    if filter_where:
        where = 'and nik ilike \'%' + filter_where + '%\' or name ilike \'%' \
                + filter_where + '%\' or jabatan ilike \'%' \
                + filter_where + '%\' or username ilike \'%' + filter_where + '%\''

    sql = text(" SELECT row_number() over (order by id) as rownum, * "
               " FROM karyawan "
               " WHERE login <> 'WEB'"
               + where +
               " ORDER BY id ")

    result = db.engine.execute(sql)

    return result
