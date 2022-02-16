from app import api, app, db
from flask import render_template, Blueprint, flash, redirect, url_for
from flask import request, Response
from flask import jsonify
from flask_login import login_required
from datetime import datetime
from fpdf import FPDF

from absensi.resource.absen import get_absen, get_rekap, get_attendance, AbsenResource
from absensi.resource.izin import get_izin, IzinResource
from absensi.resource.kegiatan import get_kegiatan, KegiatanResource
from absensi.resource.lembur import get_lembur, LemburResource
from absensi.resource.karyawan import KaryawanResource, get_karyawan

from absensi.model.model import Karyawan

import json


main = Blueprint('main', __name__)


api.add_resource(AbsenResource, '/api/absens', '/api/absens/<int:id>')
api.add_resource(IzinResource, '/api/izin', '/api/izin/<int:id>')
api.add_resource(KegiatanResource, '/api/kegiatan', '/api/kegiatan/<int:id>')
api.add_resource(LemburResource, '/api/lembur', '/api/lembur/<int:id>')
api.add_resource(KaryawanResource, '/save_karyawan', '/save_karyawan/<int:id>')


@app.route('/api/attendance')
def get_att():
    return jsonify(get_attendance(request, db))


@app.route('/absen')
@login_required
def absen():
    month_str = {
        "01": "Bulan Januari",
        "02": "Bulan Februari",
        "03": "Bulan Maret",
        "04": "Bulan April",
        "05": "Bulan Mei",
        "06": "Bulan Juni",
        "07": "Bulan Juli",
        "08": "Bulan Agustus",
        "09": "Bulan September",
        "10": "Bulan Oktober",
        "11": "Bulan November",
        "12": "Bulan Desember",
        "all": "Keseluruhan"
    }
    absens = get_absen(request, db)
    fil = request.args.get('filter')
    m = ''
    y = ''
    if fil:
        if fil == 'all':
            m = 'all'
        else:
            x = fil.split('-')
            m = x[1]
            y = x[0]
    month = month_str.get(m, "Bulan Ini")
    if fil and fil != 'all':
        month = month + " " + y

    val = ''
    if fil:
        if fil != 'all':
            val = request.args.get('filter')
    else:
        now = datetime.now()
        val = str(now.year) + "-" + str(now.month)
    return render_template('absen.html', absen=absens['data'], month=month, months=month_str, val=val)


@app.route('/izin')
@login_required
def izin():
    month_str = {
        "01": "Bulan Januari",
        "02": "Bulan Februari",
        "03": "Bulan Maret",
        "04": "Bulan April",
        "05": "Bulan Mei",
        "06": "Bulan Juni",
        "07": "Bulan Juli",
        "08": "Bulan Agustus",
        "09": "Bulan September",
        "10": "Bulan Oktober",
        "11": "Bulan November",
        "12": "Bulan Desember",
        "all": "Keseluruhan"
    }
    izins = get_izin(request, db)
    fil = request.args.get('filter')
    m = ''
    y = ''
    if fil:
        if fil == 'all':
            m = 'all'
        else:
            x = fil.split('-')
            m = x[1]
            y = x[0]
    month = month_str.get(m, "Bulan Ini")
    if fil and fil != 'all':
        month = month + " " + y

    val = ''
    if fil:
        if fil != 'all':
            val = request.args.get('filter')
    else:
        now = datetime.now()
        val = str(now.year) + "-" + str(now.month)
    return render_template('izin.html', izin=izins['data'], month=month, months=month_str, val=val)


@app.route('/kegiatan')
@login_required
def kegiatan():
    month_str = {
        "01": "Bulan Januari",
        "02": "Bulan Februari",
        "03": "Bulan Maret",
        "04": "Bulan April",
        "05": "Bulan Mei",
        "06": "Bulan Juni",
        "07": "Bulan Juli",
        "08": "Bulan Agustus",
        "09": "Bulan September",
        "10": "Bulan Oktober",
        "11": "Bulan November",
        "12": "Bulan Desember",
        "all": "Keseluruhan"
    }
    kegiatans = get_kegiatan(request, db)
    fil = request.args.get('filter')
    m = ''
    y = ''
    if fil:
        if fil == 'all':
            m = 'all'
        else:
            x = fil.split('-')
            m = x[1]
            y = x[0]
    month = month_str.get(m, "Bulan Ini")
    if fil and fil != 'all':
        month = month + " " + y

    val = ''
    if fil:
        if fil != 'all':
            val = request.args.get('filter')
    else:
        now = datetime.now()
        val = str(now.year) + "-" + str(now.month)
    return render_template('kegiatan.html', keg=kegiatans['data'], month=month, months=month_str, val=val)


@app.route('/lembur')
@login_required
def lembur():
    month_str = {
        "01": "Bulan Januari",
        "02": "Bulan Februari",
        "03": "Bulan Maret",
        "04": "Bulan April",
        "05": "Bulan Mei",
        "06": "Bulan Juni",
        "07": "Bulan Juli",
        "08": "Bulan Agustus",
        "09": "Bulan September",
        "10": "Bulan Oktober",
        "11": "Bulan November",
        "12": "Bulan Desember",
        "all": "Keseluruhan"
    }
    lemburs = get_lembur(request, db)
    fil = request.args.get('filter')
    m = ''
    y = ''
    if fil:
        if fil == 'all':
            m = 'all'
        else:
            x = fil.split('-')
            m = x[1]
            y = x[0]
    month = month_str.get(m, "Bulan Ini")
    if fil and fil != 'all':
        month = month + " " + y

    val = ''
    if fil:
        if fil != 'all':
            val = request.args.get('filter')
    else:
        now = datetime.now()
        val = str(now.year) + "-" + str(now.month)
    return render_template('lembur.html', lembur=lemburs['data'], month=month, months=month_str, val=val)


@app.route('/rekap')
@login_required
def rekap():
    month_str = {
        "01": "Bulan Januari",
        "02": "Bulan Februari",
        "03": "Bulan Maret",
        "04": "Bulan April",
        "05": "Bulan Mei",
        "06": "Bulan Juni",
        "07": "Bulan Juli",
        "08": "Bulan Agustus",
        "09": "Bulan September",
        "10": "Bulan Oktober",
        "11": "Bulan November",
        "12": "Bulan Desember",
        "all": "Keseluruhan"
    }
    rekaps = get_rekap(request, db)
    fil = request.args.get('filter')
    m = ''
    y = ''
    if fil:
        if fil == 'all':
            m = 'all'
        else:
            x = fil.split('-')
            m = x[1]
            y = x[0]
    month = month_str.get(m, "Bulan Ini")
    if fil and fil != 'all':
        month = month + " " + y

    val = ''
    if fil:
        if fil != 'all':
            val = request.args.get('filter')
    else:
        now = datetime.now()
        val = str(now.year) + "-" + str(now.month)
    return render_template('rekap.html', rekap=rekaps['data'], month=month, months=month_str, val=val)


@app.route('/download_pdf/<data>/<title>')
@login_required
def download_pdf(data, title):
    data = [data]
    result = [json.loads(idx.replace("'", '"')) for idx in data]
    pdf = PDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Times', 'B', 14)
    pdf.cell(page_width, 0, 'Rekap Data Absensi '+title, align='C')
    pdf.ln(10)

    pdf.set_font('Times', '', 10)
    pdf.set_fill_color(222, 222, 222)

    pdf.ln(1)
    th = pdf.font_size + 5

    table_col_names = ("No", "NIK", "Nama", "Total Absen Masuk")
    col_widths = [20, 49, 70, 50]
    col_align = ["C", "", "", "C"]

    def render_table_header():
        pdf.set_font(style="B")  # enabling bold text
        for idx, val in enumerate(table_col_names):
            pdf.cell(col_widths[idx], th, val, border=1, align='C', fill=True)
        pdf.ln(th)
        pdf.set_font(style="")

    render_table_header()

    pdf.set_fill_color(255, 255, 255)

    for row in result[0]:
        for idx, datum in enumerate(row):
            pdf.multi_cell(col_widths[idx], th, str(row[datum]), border=1, ln=3,
                           max_line_height=pdf.font_size, align=col_align[idx])
        pdf.ln(th)

    return Response(pdf.output(dest='S'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=rekap_karyawan.pdf'})


@app.route('/download_pdf_izin/<data>/<title>')
@login_required
def download_pdf_izin(data, title):
    data = [data]
    result = [json.loads(idx.replace("'", '"')) for idx in data]

    pdf = PDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Times', 'B', 14)
    pdf.cell(page_width, 0, 'Rekap Izin '+title, align='C')
    pdf.ln(10)

    pdf.set_font('Times', '', 10)
    pdf.set_fill_color(222, 222, 222)

    pdf.ln(1)
    th = pdf.font_size + 5

    table_col_names = ("No", "NIK", "Nama", "Posisi", "Jabatan", "Tanggal", "Waktu", "Keterangan")
    col_widths = [10, 17, 35, 25, 25, 20, 20, 37]
    col_align = ["C", "", "", "", "", "C", "C", "L"]

    def render_table_header():
        pdf.set_font(style="B")  # enabling bold text
        for idx, val in enumerate(table_col_names):
            pdf.cell(col_widths[idx], th, val, border=1, align='C', fill=True)
        pdf.ln(th)
        pdf.set_font(style="")

    render_table_header()

    pdf.set_fill_color(255, 255, 255)

    for row in result[0]:
        for idx, datum in enumerate(row):
            pdf.multi_cell(col_widths[idx], th, str(row[datum]), border=1, ln=3,
                           max_line_height=pdf.font_size, align=col_align[idx])
        pdf.ln(th)

    return Response(pdf.output(dest='S'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=rekap_karyawan_izin.pdf'})


@app.route('/download_pdf_lembur/<data>/<title>')
@login_required
def download_pdf_lembur(data, title):
    data = [data]
    result = [json.loads(idx.replace("'", '"')) for idx in data]

    pdf = PDF()
    pdf.add_page()

    page_width = pdf.w - 2 * pdf.l_margin

    pdf.set_font('Times', 'B', 14)
    pdf.cell(page_width, 0, 'Rekap Lembur '+title, align='C')
    pdf.ln(10)

    pdf.set_font('Times', '', 10)
    pdf.set_fill_color(222, 222, 222)

    pdf.ln(1)
    th = pdf.font_size + 5

    table_col_names = ("No", "NIK", "Nama", "Posisi", "Jabatan", "Tanggal", "Waktu", "Keterangan")
    col_widths = [10, 17, 35, 25, 25, 20, 20, 37]
    col_align = ["C", "", "", "", "", "C", "C", "L"]

    def render_table_header():
        pdf.set_font(style="B")  # enabling bold text
        for idx, val in enumerate(table_col_names):
            pdf.cell(col_widths[idx], th, val, border=1, align='C', fill=True)
        pdf.ln(th)
        pdf.set_font(style="")

    render_table_header()

    pdf.set_fill_color(255, 255, 255)

    for row in result[0]:
        for idx, datum in enumerate(row):
            pdf.multi_cell(col_widths[idx], th, str(row[datum]), border=1, ln=3,
                           max_line_height=pdf.font_size, align=col_align[idx])
        pdf.ln(th)

    return Response(pdf.output(dest='S'), mimetype='application/pdf',
                    headers={'Content-Disposition': 'attachment;filename=rekap_karyawan_lembur.pdf'})


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
            if str(request.form.get("nik")) != str(karyawan.nik):
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
        karyawan.posisi = request.form.get("posisi")
        karyawan.jabatan = request.form.get("jabatan")
        karyawan.username = request.form.get("username")
        karyawan.password = request.form.get("password")
        karyawan.login = "MOBILE"

        if isnew:
            db.session.add(karyawan)
        db.session.commit()
        return redirect(url_for('karyawan'))
    kar = {'id': None, 'nik': '', 'name': '', 'posisi': '', 'jabatan': '', 'username': '', 'password': ''}
    if id:
        kar = get_karyawan(request, db, id)
        if kar == {}:
            flash('id tidak ditemukan')
            return redirect(url_for('form_karyawan'))
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


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"- Page {self.page_no()}/{{nb}} -", 0, 0, "C")