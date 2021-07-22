from app import db, ma
from flask_login import UserMixin


class Karyawan(UserMixin, db.Model):
    __tabelname__ = 'karyawan'
    __table_args__ = {'extend_existing': True}
    # absen = db.relationship("Absen", uselist=False, back_populates="karyawan")


class Absen(db.Model):
    __tabelname__ = 'absen'
    __table_args__ = {'extend_existing': True}
    # nik = db.column(db.Integer, db.ForeignKey("karyawan.nik"))
    # karyawan = db.relationship("Karyawan", back_populates="absen")


class KaryawanSchema(ma.ModelSchema):
    class Meta:
        model = Karyawan


class AbsenSchema(ma.ModelSchema):
    # karyawan = ma.Nested(KaryawanSchema, many=False)

    class Meta:
        model = Absen
