from sqlalchemy import Column, Integer, String, DOUBLE, ForeignKey, BOOLEAN, Enum, LargeBinary, DATETIME
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from __init__ import app, db
from flask_login import UserMixin
import hashlib
import enum
import os
import datetime


class UserRole(enum.Enum):
    khach_hang = 1
    le_tan = 2
    quan_ly = 3


class LoaiKhach(enum.Enum):
    noi_dia = 1
    nuoc_ngoai = 2


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(45), unique=True, nullable=True)
    password = Column(String(45), nullable=True)
    ho = Column(String(22), nullable=False)
    ten = Column(String(45), nullable=False)
    gioi_tinh = Column(BOOLEAN, nullable=False, default=False)
    ngay_sinh = Column(DATETIME, nullable=True)
    cccd = Column(String(15), nullable=False, unique=True)
    sdt = Column(String(12))
    email = Column(String(30))
    dia_chi = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.quan_ly)

    def __str__(self):
        return self.name


class KhachHang(User):
    id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable=False)
    loai_khach = Column(Enum(LoaiKhach), nullable=False, default=LoaiKhach.noi_dia)

    def dat_phong(self):
        pass


class LeTan(User):
    id = Column(Integer, ForeignKey(User.id), primary_key=True, nullable=False)
    luong = Column(DOUBLE, nullable=False, default=1000)

    def cho_thue_phong(self):
        pass


class LoaiPhong(db.Model):
    id = Column(String(10), primary_key=True, nullable=False)
    loai_phong = Column(String(30), nullable=False)
    mo_ta = Column(String(300), default="")
    dien_tich = Column(DOUBLE, nullable=False)
    cac_phong = relationship("Phong", backref="LoaiPhong", lazy=True)

    def __str__(self):
        return self.loai_phong


# tiennghi
class TienNghi(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ten = Column(String(45), nullable=False)
    tinh_trang = Column(BOOLEAN, nullable=False, default=True)
    gia_tien = Column(DOUBLE, nullable=False, default=100)


# loaiphong -- tiennghi
class LoaiPhong_TienNghi(db.Model):
    id_loaiphong = Column(String(10), ForeignKey(LoaiPhong.id), primary_key=True, nullable=False)
    id_tiennghi = Column(Integer, ForeignKey(TienNghi.id), primary_key=True, nullable=False)
    so_luong = Column(Integer, nullable=False, default=1)


# dich vu
class DichVu(db.Model):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    ten = Column(String(45), nullable=False)
    tinh_trang = Column(BOOLEAN, nullable=False, default=True)
    gia_tien = Column(DOUBLE, nullable=False, default=0)


# loaiphong -- dichvu
class LoaiPhong_DichVu(db.Model):
    id_loaiphong = Column(String(10), ForeignKey(LoaiPhong.id), primary_key=True, nullable=False)
    id_dichvu = Column(Integer, ForeignKey(DichVu.id), primary_key=True, nullable=False)


# PHONG
class Phong(db.Model):
    id = Column(String(10), primary_key=True, nullable=False)
    tinh_trang = Column(BOOLEAN, nullable=False, default=True)
    id_loaiphong = Column(String(45), ForeignKey(LoaiPhong.id), primary_key=True, nullable=False)


# khach hang - phong
class ThoiGianTraThuePhong(db.Model):
    id_khachhang = Column(Integer, ForeignKey(KhachHang.id), nullable=False, primary_key=True)
    id_phong = Column(String(3), ForeignKey(Phong.id), primary_key=True, nullable=False)
    thoi_gian_thue = Column(DATETIME, nullable=False, primary_key=True)
    thoi_gian_tra = Column(DATETIME, nullable=False, primary_key=True)


class NguoiDatPhong(db.Model):
    id_user = Column(Integer, ForeignKey(User.id), nullable=False, primary_key=True)
    id_phong = Column(String(10), ForeignKey(Phong.id), nullable=False, primary_key=True)
    thoi_gian_dat = Column(DATETIME, nullable=False, primary_key=True)


class HoaDon(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)


class ChiTietHoaDon(db.Model):
    id_phong = Column(String(10), ForeignKey(Phong.id), nullable=False, primary_key=True)
    id_hoadon = Column(Integer, ForeignKey(HoaDon.id), nullable=False, primary_key=True)
    don_gia = Column(DOUBLE, nullable=False)


if __name__ == "__main__":
    with app.app_context():
        r""
        db.drop_all()
        db.create_all()
        # cki = datetime.datetime(year=datetime.datetime.today().year, month=1, day=8)
        # cko = datetime.datetime(year=datetime.datetime.today().year, month=1, day=10)
        # rent1 = ThoiGianTraThuePhong(id_khachhang=1, id_phong="103", thoi_gian_thue=cki, thoi_gian_tra=cko)
        # # cki = datetime.datetime(year=datetime.datetime.today().year, month=2, day=18)
        # cko = datetime.datetime(year=datetime.datetime.today().year, month=2, day=22)
        # rent2 = ThoiGianTraThuePhong(id_khachhang=1, id_phong="301", thoi_gian_thue=cki, thoi_gian_tra=cko)
        # cki = datetime.datetime(year=datetime.datetime.today().year, month=2, day=1)
        # cko = datetime.datetime(year=datetime.datetime.today().year, month=2, day=13)
        # rent3 = ThoiGianTraThuePhong(id_khachhang=1, id_phong="301", thoi_gian_thue=cki, thoi_gian_tra=cko)
        # db.session.add_all([rent1, rent2, rent3])
        # db.session.commit()

        admin = User(username='admin', password=str(hashlib.md5('123'.encode("utf-8")).hexdigest()), ho='admin', ten ='admin', ngay_sinh=datetime.datetime.today(), cccd='123')







