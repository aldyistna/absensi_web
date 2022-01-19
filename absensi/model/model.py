from app import db, ma
from flask_login import UserMixin


class Karyawan(UserMixin, db.Model):
    __tabelname__ = 'karyawan'
    __table_args__ = {'extend_existing': True}


class Absen(db.Model):
    __tabelname__ = 'absen'
    __table_args__ = {'extend_existing': True}


class Izin(db.Model):
    __tabelname__ = 'izin'
    __table_args__ = {'extend_existing': True}


class Kegiatan(db.Model):
    __tabelname__ = 'kegiatan'
    __table_args__ = {'extend_existing': True}


class Lembur(db.Model):
    __tabelname__ = 'lembur'
    __table_args__ = {'extend_existing': True}


class KaryawanSchema(ma.ModelSchema):
    class Meta:
        model = Karyawan


class AbsenSchema(ma.ModelSchema):
    class Meta:
        model = Absen


class IzinSchema(ma.ModelSchema):
    class Meta:
        model = Izin


class KegiatanSchema(ma.ModelSchema):
    class Meta:
        model = Kegiatan


class LemburSchema(ma.ModelSchema):
    class Meta:
        model = Lembur
