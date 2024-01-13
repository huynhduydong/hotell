import hashlib
import math

from sqlalchemy import func, cast

from models import *
from app import db


def authenticate_user(username, password):
    return (db.session.query(User)
            .filter(User.username == username,
                    User.password == hashlib.md5(password.encode('utf-8')).hexdigest()).first())


def get_user_by_id(user_id):
    return db.session.query(User).filter(User.id == user_id).first()

def dat_phong(ten_nguoi_dat, ngay_dat_phong, ngay_tra_phong, phong, khach_hang):
    so_nguoi_trung_binh_tren_1_phong = math.ceil(len(khach_hang) / len(phong))
    quy_dinh_so_nguoi_toi_da = db.session.query(QuyDinh).filter(QuyDinh.key == QuyDinhEnum.SO_KHACH_TOI_DA_TRONG_PHONG)

    if so_nguoi_trung_binh_tren_1_phong > quy_dinh_so_nguoi_toi_da:
        raise Exception(f'Dat qua so nguoi toi da ({quy_dinh_so_nguoi_toi_da})')

    phieu_dat_phong = PhieuDatPhong(ten_nguoi_dat=ten_nguoi_dat, ngay_dat_phong=ngay_dat_phong,
                                    ngay_tra_phong=ngay_tra_phong)
    db.session.add(phieu_dat_phong)

    for id_phong in phong:
        p = db.session.query(Phong).filter(Phong.id.__eq__(int(id_phong)), Phong.tinh_trang == TinhTrangPhongEnum.TRONG).first()
        if p is None:
            raise Exception('Phong khong hop le')

        chi_tiet_dat_phong = ChiTietDatPhong(id_phong=id_phong, id_phieu_dat_phong=phieu_dat_phong.id,
                                             don_gia=p.don_gia)
        db.session.add(chi_tiet_dat_phong)
        p.tinh_trang = TinhTrangPhongEnum.DA_DAT

    db.session.add(phieu_dat_phong)

    for kh in khach_hang:
        n_kh = KhachHang(ten_khach_hang=kh['ten_khach_hang'], loai_khach_hang=KhachHangEnum[kh['loai_khach_hang']],
                         cmnd=kh['cmnd'], dia_chi=kh['dia_chi'], id_phieu_dat_phong=phieu_dat_phong.id)
        db.session.add(n_kh)
    db.session.commit()

    return phieu_dat_phong


def stats_sale(from_date, to_date):
    stats_data = (db.session.query(Phong.loai_phong,
                                   cast(func.sum(ChiTietDatPhong.don_gia).label(''), Integer),
                                   func.count(ChiTietDatPhong.id_phieu_dat_phong))
                  .join(ChiTietDatPhong)
                  .join(PhieuDatPhong)
                  .group_by(Phong.loai_phong)
                  .filter(PhieuDatPhong.ngay_tra_phong.between(from_date, to_date))
                  .all())

    return [{'loai_phong': loai_phong.name, 'doanh_thu': doanh_thu, 'luot_thue': luot_thue}
            for loai_phong, doanh_thu, luot_thue in stats_data]


def phieu_dat_sang_phieu_thue(id_phieu_dat):
    pdp = db.session.query(PhieuDatPhong).filter(PhieuDatPhong.id.__eq__(int(id_phieu_dat))).first()
    if pdp is None:
        return

    for ctdt in pdp.cac_chi_tiet_dat_phong:
        ctdt.phong.tinh_trang = TinhTrangPhongEnum.DANG_O

    ptp = PhieuThuePhong(id_phieu_dat_phong=pdp.id)
    db.session.add(ptp)

    db.session.commit()


def get_phong_trong():
    return db.session.query(Phong).filter(Phong.tinh_trang == TinhTrangPhongEnum.TRONG).all()


def tinh_tien_phong(phong, khach_hang):
    return None