from datetime import datetime, time, timedelta
import calendar
import time
from flask_restful import Resource, request, reqparse
from sqlalchemy import text

import werkzeug
import os
from firebase_upload import upload_file
from absensi.model.model import Absen, AbsenSchema

from app import app, db

parser = reqparse.RequestParser()
parser.add_argument('nik', required=True, help='nik parameter is required')
parser.add_argument('id', required=False, help='nik parameter is required')
parser.add_argument('location', required=True, help='location parameter is required')
parser.add_argument('date', required=True, help='date parameter is required')
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)


def get_absen(requests, dbs):
    sql_where = " WHERE EXTRACT(Month from time_in) = EXTRACT(MONTH from now()) "

    fil = requests.args.get('filter')
    if fil:
        if fil == 'all':
            sql_where = ''
        else:
            ym = fil.split("-")
            sql_where = " WHERE EXTRACT(YEAR from time_in) = " + ym[0] + " AND EXTRACT(MONTH from time_in) = " + ym[1]

    sql = text(" SELECT row_number() over (order by time_in::date desc, time_in::time(0)) as rownum, "
               " b.nik as nik, b.name as name, "
               " time_in::date as date_in, time_in::time(0) as time_in,"
               " coalesce(time_out::date::varchar, '-')  as date_out, "
               " coalesce(time_out::time(0)::varchar, '-') as time_out, "
               " location_in, coalesce(location_out, '-') as location_out, "
               " url_photo_in, url_photo_out "
               " FROM absen a "
               " JOIN karyawan b on a.nik = b.nik "
               + sql_where +
               " ORDER BY date_in desc, time_in ")

    result = dbs.engine.execute(sql)

    return {
        'data': [dict(row) for row in result]
    }


def get_rekap(requests, dbs):
    sql_where = " AND EXTRACT(Month from time_in) = EXTRACT(MONTH from now()) "
    sql_where_izin = " AND EXTRACT(Month from i.date) = EXTRACT(MONTH from now()) "
    sql_where_lembur = " AND EXTRACT(Month from l.date) = EXTRACT(MONTH from now()) "

    fil = requests.args.get('filter')
    if fil:
        if fil == 'all':
            sql_where = ''
            sql_where_izin = ''
            sql_where_lembur = ''
        else:
            ym = fil.split("-")
            sql_where = " AND EXTRACT(YEAR from time_in) = " + ym[0] + " AND EXTRACT(MONTH from time_in) = " + ym[1]
            sql_where_izin = " AND EXTRACT(YEAR from i.date) = " + ym[0] + " AND EXTRACT(MONTH from i.date) = " + ym[1]
            sql_where_lembur = "AND EXTRACT(YEAR from l.date) = " + ym[0] + " AND EXTRACT(MONTH from l.date) = " + ym[1]

    sql = text(" SELECT row_number() over (order by name) as rownum, "
               " a.nik, a.name, count(b.time_in) as total_absen_masuk, "
               " count(b.time_out) as total_absen_pulang, "
               " count(distinct i.date) as total_izin, count(distinct l.date) as total_lembur "
               " FROM karyawan a "
               " LEFT JOIN absen b on a.nik = b.nik " + sql_where +
               " LEFT JOIN izin i on a.nik = i.nik " + sql_where_izin +
               " LEFT JOIN lembur l on a.nik = l.nik " + sql_where_lembur +
               " WHERE a.login <> 'WEB' "
               " GROUP BY a.nik, a.name "
               " ORDER BY name ")

    result = dbs.engine.execute(sql)

    # return result
    return {
        'data': [dict(row) for row in result]
    }


def get_attendance(requests, dbs):
    date = requests.args.get('date')
    nik = requests.args.get('nik')

    sql = text(" select nik, sum(absen_in)::varchar as absen_in, sum(absen_out)::varchar as absen_out,"
               " sum(izin)::varchar as izin, sum(lembur)::varchar as lembur"
               " from ("
               " SELECT nik, count(time_in) as absen_in, count(time_out) as absen_out, 0 as izin, 0 as lembur"
               " FROM absen"
               " where nik = '" + nik + "'"
               " and to_char(time_in, 'YYYY-MM-DD') = '" + date + "'"
               " group by nik "
               " union"
               " SELECT nik, 0 as absen_in, 0 as absen_out, count(date) as izin, 0 as lembur"
               " FROM izin"
               " where nik = '" + nik + "'"
               " and to_char(date, 'YYYY-MM-DD') = '" + date + "'"
               " group by nik "
               " union"
               " SELECT nik, 0 as absen_in, 0 as absen_out, 0 as izin, count(date) as lembur"
               " FROM lembur"
               " where nik =' " + nik + "'"
               " and to_char(date, 'YYYY-MM-DD') = '" + date + "'"
               " group by nik "
               " ) T"
               " group by nik")

    result = dbs.engine.execute(sql)

    return {
        'data': [dict(row) for row in result]
    }


class AbsenResource(Resource):
    decorators = []

    def post(self, id=None):
        data = parser.parse_args()
        date_name = calendar.timegm(time.gmtime())
        if data['file'] == "":
            return {
                'data': '',
                'message': 'No file found',
                'status': 'error'
            }
        image = data['file']
        ext = image.filename.split('.')[-1]
        filename = 'absen_' + str(date_name) + '.' + ext
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        isnew = False
        if id:
            absen = Absen.query.filter_by(id=id).first()
            absen.location_out = data['location']
            absen.time_out = data['date']
            absen.url_photo_out = upload_file('absen_out/' + filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))
        else:
            absen = Absen()
            isnew = True
            absen.nik = data['nik']
            absen.location_in = data['location']
            absen.time_in = data['date']
            absen.url_photo_in = upload_file('absen_in/' + filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if isnew:
            db.session.add(absen)
        db.session.commit()
        db.session.refresh(absen)

        absen_scheme = AbsenSchema()
        output = absen_scheme.dump(absen).data
        return {
            'data': output,
            'message': 'Post data succeeded',
            'status': 'success'
        }

    def get(self, id=None):
        if id:
            absen_schema = AbsenSchema()
            absen = Absen.query.filter_by(id=id).first()
            return {
                'data': absen_schema.dump(absen).data,
                'message': 'Success',
                'status': 'Success'
            }
        else:
            args = request.args.to_dict()
            date = args.get('date')

            args.pop('date', None)

            absen = Absen.query.filter_by(**args)

            if date is not None:
                date_object = datetime.strptime(date, '%Y-%m-%d')
                absen = absen.filter(Absen.time_in >= date_object)\
                    .filter(Absen.time_in < date_object + timedelta(hours=24))

            absen = absen.order_by(Absen.time_in.desc())
            total_data = absen.count()

            absen_scheme = AbsenSchema(many=True)

            output = absen_scheme.dump(absen).data

            return {
                'totalData': total_data,
                'data': output
            }
