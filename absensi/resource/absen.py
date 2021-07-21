from datetime import datetime, time, timedelta

from sqlalchemy import text


def get_absen(request, db):
    sql = text(" SELECT b.nik as nik, b.name as name, "
               " time_in::date as date_in, time_in::time(0) as time_in,"
               " time_out::date as date_out, time_out::time(0) as time_out, "
               " location_in, location_out, url_photo_in, url_photo_out "
               " FROM absen a "
               " JOIN karyawan b on a.nik = b.nik "
               " ORDER BY date_in desc, time_in ")

    result = db.engine.execute(sql)

    return result
