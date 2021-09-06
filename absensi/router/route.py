from app import api, app, db
from flask import render_template, Blueprint
from flask import request
from flask_login import login_required

from absensi.resource.absen import get_absen, get_rekap, AbsenResource
from absensi.resource.karyawan import KaryawanResource


main = Blueprint('main', __name__)


api.add_resource(AbsenResource, '/api/absens', '/api/absens/<int:id>')
api.add_resource(KaryawanResource, '/save_karyawan')


@app.route('/absen')
@login_required
def absen():
    absen = get_absen(request, db)
    return render_template('absen.html', absen=absen)


@app.route('/rekap')
@login_required
def rekap():
    rekap = get_rekap(request, db)
    return render_template('rekap.html', rekap=rekap)


@app.route('/add_karyawan', methods=["POST", "GET"])
@login_required
def add_karyawan():
    if request.method == "POST":
        print(request.form)
    return render_template('add_karyawan.html')

