# import sys
from app import db, ma


class Karyawan(db.Model):
    __tabelname__ = 'karyawan'
    __table_args__ = {'extend_existing': True}
    nik = db.Column(db.Integer, primary_key=True)
    # laporan = db.relationship("Laporan", uselist=False, back_populates="user")


class Absen(db.Model):
    __tabelname__ = 'absen'
    __table_args__ = {'extend_existing': True}
    # dibuat_oleh = db.Column(db.String, db.ForeignKey("users.username"))
    # user = db.relationship('Users', back_populates="laporan")


class KaryawanSchema(ma.ModelSchema):
    class Meta:
        model = Karyawan


class AbsenSchema(ma.ModelSchema):
    class Meta:
        model = Absen
