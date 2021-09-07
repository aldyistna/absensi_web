from app import api, app, db
from flask import render_template, Blueprint, flash, redirect, url_for
from flask import request
from flask_login import login_required

from absensi.resource.absen import get_absen, get_rekap, AbsenResource
from absensi.resource.karyawan import KaryawanResource, get_karyawan

from absensi.model.model import Karyawan


main = Blueprint('main', __name__)


api.add_resource(AbsenResource, '/api/absens', '/api/absens/<int:id>')
api.add_resource(KaryawanResource, '/save_karyawan', '/save_karyawan/<int:id>')


@app.route('/absen')
@login_required
def absen():
    absens = get_absen(request, db)
    return render_template('absen.html', absen=absens)


@app.route('/rekap')
@login_required
def rekap():
    rekaps = get_rekap(request, db)
    return render_template('rekap.html', rekap=rekaps)


@app.route('/form_karyawan', methods=["POST", "GET"])
@app.route('/form_karyawan/<id>', methods=["POST", "GET"])
@login_required
def form_karyawan(id=None):
    if request.method == "POST":
        isnew = False
        if request.form.get("id") is None:
            isnew = True
            karyawan = Karyawan()
            nik_check = Karyawan.query.filter_by(nik=request.form.get("nik")).first()
            if nik_check:
                flash('NIK sudah digunakan !')
                return redirect(request.url)
            uname_check = Karyawan.query.filter_by(username=request.form.get("username")).first()
            if uname_check:
                flash('Username sudah digunakan !')
                return redirect(request.url)
        else:
            karyawan = Karyawan.query.filter_by(id=request.form.get("id")).first()
            if request.form.get("nik") != karyawan.nik:
                nik_check = Karyawan.query.filter_by(nik=request.form.get("nik")).first()
                if nik_check:
                    flash('NIK sudah digunakan !')
                    return redirect(request.url)

            if request.form.get("username") != karyawan.username:
                uname_check = Karyawan.query.filter_by(username=request.form.get("nik")).first()
                if uname_check:
                    flash('Username sudah digunakan !')
                    return redirect(request.url)

        karyawan.nik = request.form.get("nik")
        karyawan.name = request.form.get("name")
        karyawan.jabatan = request.form.get("jabatan")
        karyawan.username = request.form.get("username")
        karyawan.password = request.form.get("password")
        karyawan.login = "MOBILE"

        if isnew:
            db.session.add(karyawan)
        db.session.commit()
        return redirect(url_for('karyawan'))
    kar = {'id': None, 'nik': '', 'name': '', 'jabatan': '', 'username': '', 'password': ''}
    if id:
        kar = get_karyawan(request, db, id)
        if kar == {}:
            flash('id tidak ditemukan')
            return redirect(url_for('form_karyawan'))
    print(kar)
    return render_template('add_karyawan.html', id=id, kar=kar)


@app.route('/karyawan')
@login_required
def karyawan():
    kar = get_karyawan(request, db)
    return render_template('karyawan.html', kar=kar)


@app.errorhandler(404)
def e404(e):
    return http_err(404)


def http_err(err_code):

    if 400 == err_code:
        err_msg = "It seems like you are not allowed to access this link."

    elif 404 == err_code:
        err_msg = "The URL you were looking for does not seem to exist."
        err_msg += "<br /> Define the new page in themes/phantom/pages"

    elif 500 == err_code:
        err_msg = "Internal error. Contact the manager about this."

    else:
        err_msg = "Forbidden access."

    return err_msg

