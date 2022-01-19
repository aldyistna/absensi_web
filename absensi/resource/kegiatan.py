from datetime import datetime, time, timedelta
import calendar
import time
from flask_restful import Resource, request, reqparse
from sqlalchemy import text

import werkzeug
import os
from firebase_upload import upload_file
from absensi.model.model import Kegiatan, KegiatanSchema

from app import app, db

parser = reqparse.RequestParser()
parser.add_argument('nik', required=True, help='nik parameter is required')
parser.add_argument('keterangan', required=True, help='keterangan parameter is required')
parser.add_argument('date', required=True, help='date parameter is required')
parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files', required=True)


def get_kegiatan(requests, dbs):
    sql_where = " WHERE EXTRACT(Month from date) = EXTRACT(MONTH from now()) "

    fil = requests.args.get('filter')
    if fil:
        if fil == 'all':
            sql_where = ''
        else:
            ym = fil.split("-")
            sql_where = " WHERE EXTRACT(YEAR from date) = " + ym[0] + " AND EXTRACT(MONTH from date) = " + ym[1]

    sql = text(" SELECT row_number() over (order by date::date desc, date::time(0)) as rownum, "
               " b.nik as nik, b.name as name, "
               " date::date as tanggal, date::time(0) as waktu, keterangan, url_photo "
               " FROM kegiatan a "
               " JOIN karyawan b on a.nik = b.nik "
               + sql_where +
               " ORDER BY tanggal desc, waktu ")

    result = dbs.engine.execute(sql)

    return {
        'data': [dict(row) for row in result]
    }


class KegiatanResource(Resource):
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
        filename = 'keg_' + str(date_name) + '.' + ext
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        keg = Kegiatan()
        keg.nik = data['nik']
        keg.keterangan = data['keterangan']
        keg.date = data['date']
        keg.url_photo = upload_file('kegiatan/' + filename, os.path.join(app.config['UPLOAD_FOLDER'], filename))

        db.session.add(keg)
        db.session.commit()
        db.session.refresh(keg)

        keg_scheme = KegiatanSchema()

        output = keg_scheme.dump(keg).data
        return {
            'data': output,
            'message': 'Post data succeeded',
            'status': 'success'
        }
