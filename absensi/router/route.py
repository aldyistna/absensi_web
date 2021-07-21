from app import api, app, db
from flask import render_template
from flask import request

from absensi.resource.absen import get_absen


@app.route('/absen')
def index():
    absen = get_absen(request, db)
    return render_template('absen.html', absen=absen)
