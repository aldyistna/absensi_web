from flask_restful import Resource, reqparse, request
from datetime import datetime, timedelta
from sqlalchemy import text

from absensi.model.model import Lembur, LemburSchema

from app import db

parser = reqparse.RequestParser()
parser.add_argument('nik', required=True, help='nik parameter is required')
parser.add_argument('keterangan', required=True, help='keterangan parameter is required')
parser.add_argument('date', required=True, help='date parameter is required')


def get_lembur(requests, dbs):
    sql_where = " WHERE EXTRACT(Month from date) = EXTRACT(MONTH from now()) "

    fil = requests.args.get('filter')
    if fil:
        if fil == 'all':
            sql_where = ''
        else:
            ym = fil.split("-")
            sql_where = " WHERE EXTRACT(YEAR from date) = " + ym[0] + " AND EXTRACT(MONTH from date) = " + ym[1]

    sql = text(" SELECT row_number() over (order by date::date desc, date::time(0)) as rownum, "
               " b.nik , b.name, b.posisi, b.jabatan, "
               " date::date as tanggal, date::time(0) as waktu, keterangan "
               " FROM lembur a "
               " JOIN karyawan b on a.nik = b.nik "
               + sql_where +
               " ORDER BY tanggal desc, waktu ")

    result = dbs.engine.execute(sql)

    return {
        'data': [dict(row) for row in result]
    }


class LemburResource(Resource):
    decorators = []

    def post(self, id=None):
        data = parser.parse_args()

        lembur = Lembur()
        lembur.nik = data['nik']
        lembur.keterangan = data['keterangan']
        lembur.date = data['date']

        db.session.add(lembur)
        db.session.commit()
        db.session.refresh(lembur)

        lembur_scheme = LemburSchema()

        output = lembur_scheme.dump(lembur).data
        return {
            'data': output,
            'message': 'Post data succeeded',
            'status': 'success'
        }

    def get(self, id=None):
        if id:
            absen_schema = LemburSchema()
            absen = Lembur.query.filter_by(id=id).first()
            return {
                'data': absen_schema.dump(absen).data,
                'message': 'Success',
                'status': 'Success'
            }
        else:
            args = request.args.to_dict()
            date = args.get('date')

            args.pop('date', None)

            absen = Lembur.query.filter_by(**args)

            if date is not None:
                date_object = datetime.strptime(date, '%Y-%m-%d')
                absen = absen.filter(Lembur.date >= date_object)\
                    .filter(Lembur.date < date_object + timedelta(hours=24))

            absen = absen.order_by(Lembur.date.desc())
            total_data = absen.count()

            absen_scheme = LemburSchema(many=True)

            output = absen_scheme.dump(absen).data

            return {
                'totalData': total_data,
                'data': output
            }
