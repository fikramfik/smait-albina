from albina import db, login_menager
from datetime import datetime
from flask_login import UserMixin

@login_menager.user_loader
def load_user(dt_daftar_id):
    return Dt_daftar.query.get(int(dt_daftar_id))

#@login_menager.user_loader
#def load_user(dt_admin_id):
    return Dt_admin.query.get(int(dt_admin_id))



class Dt_daftar(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    niss= db.Column(db.String(15), unique=True, nullable=False)
    nm_siswa= db.Column(db.String(20), nullable=True)
    tmpt_lhr = db.Column(db.String(10), nullable=True)
    tgl_lhr = db.Column(db.String(10), nullable=True)
    jk= db.Column(db.String(10), nullable=True)
    almt_siswa = db.Column(db.String(20), nullable=True)
    agama= db.Column(db.String(20), nullable=True)
    nm_ortu = db.Column(db.String(20), nullable=True)
    telp_ortu = db.Column(db.String(12), nullable=True)
    password = db.Column(db.String(10), nullable=False)
    gmbr = db.Column(db.String(10), nullable=True)
    def __repr__(self):
        return f"Dt_daftar('{self.niss}','{self.nm_siswa}','{self.tmpt_lhr}','{self.tgl_lhr}','{self.jk}','{self.almt_siswa}','{self.agama}','{self.nm_ortu}','{self.telp_ortu}','{self.password}','{self.gmbr})"
        


class Dt_profil(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    profil= db.Column(db.String(200), nullable=False)
    visi= db.Column(db.String(100), nullable=False)
    misi=db.Column(db.String(100), nullable=False)
    gmbr= db.Column(db.String(10), nullable=True)
    def __repr__(self):
        return f"Dt_profil('{self.profil}','{self.visi}','{self.misi}','{self.gmbr}')"



class Dt_sarana(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    sarana= db.Column(db.String(100), nullable=False)
    gmbr= db.Column(db.String(5), nullable=True)
    ket= db.Column(db.String(50), nullable=True)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Dt_sarana('{self.gmbr}','{self.ket}','{self.tgl_post}')"


class Dt_galeri(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    gmbr= db.Column(db.String(5), nullable=True)
    ket= db.Column(db.String(50), nullable=True)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    def __repr__(self):
        return f"Dt_galeri('{self.gmbr}','{self.ket}','{self.tgl_post}')"



class Dt_program(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    program= db.Column(db.String(10), nullable=False)
    gmbr= db.Column(db.String(5), nullable=True)
    ket= db.Column(db.String(50), nullable=True)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    beritat = db.relationship('Dt_berita', backref='programberita',lazy=True)
    def __repr__(self):
        return f"Dt_program('{self.program}','{self.gmbr}','{self.ket}','{self.tgl_post}')"


class Dt_kegiatan(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    kegiatan= db.Column(db.String(10), nullable=False)
    gmbr= db.Column(db.String(5), nullable=True)
    ket= db.Column(db.String(50), nullable=True)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    beritak = db.relationship('Dt_berita', backref='kegiatanberita',lazy=True)
    def __repr__(self):
        return f"Dt_kegiatan('{self.kegiatan}','{self.gmbr}','{self.ket}','{self.tgl_post}')"


class Dt_berita(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    berita= db.Column(db.String(10), nullable=False)
    gmbr= db.Column(db.String(5), nullable=True)
    ket= db.Column(db.String(50), nullable=True)
    tgl_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    id_prgram = db.Column (db.Integer, db.ForeignKey('dt_program.id'))
    id_kegiatan = db.Column (db.Integer, db.ForeignKey('dt_kegiatan.id'))

    def __repr__(self):
        return f"Dt_berita('{self.berita}','{self.gmbr}','{self.ket}','{self.tgl_post})"

class Dt_admin(db.Model, UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    nip = db.Column(db.String(10), unique=True, nullable=False)
    nama = db.Column(db.String(15), nullable=True)
    password = db.Column(db.String(10), nullable=True)
    gmbr= db.Column(db.String(5), nullable=True)
    def __repr__(self):
        return f"Dt_admin('{self.nip}','{self.nama}','{self.password}','{self.gmbr}')"

