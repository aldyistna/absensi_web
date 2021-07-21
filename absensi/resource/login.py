
from flask_restful import Resource, reqparse

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

        karyawan = Karyawan.query.filter(Karyawan.nik == nik) \
            .filter(Karyawan.password == password) \
            .filter(Karyawan.login == login).first()

        karyawan_schema = KaryawanSchema()
        output = karyawan_schema.dump(karyawan).data
        if output:
            return {
                'status': 1,
                'message': 'success',
                'data': output
            }
        else:
            return {
                'status': 0,
                'message': 'failed',
                'data': ''
            }
