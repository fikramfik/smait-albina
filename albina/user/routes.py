from operator import add
from types import prepare_class
from flask import Flask, Blueprint,flash, render_template, url_for, redirect, request
from albina import db, bcrypt
from albina import app
from flask_wtf import file
from wtforms import form
from wtforms.validators import DataRequired, Email
from albina.dtbase import Dt_daftar,Dt_berita, Dt_profil,Dt_program,Dt_kegiatan,Dt_galeri,Dt_sarana # Tabel bagian database
from albina.user.forms import daftar_siswa, login_siswa, updt_siswa
from flask_login import login_user, logout_user, current_user, login_required
from PIL import Image
import os
import secrets

buser= Blueprint('buser',__name__)

#####################################################################################################################

#simpan foto
def simpan_gambar(form_gmbr):
    random_hex= secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_gmbr.filename)
    foto_fn= random_hex + f_ext
    foto_path= os.path.join(app.root_path, 'albina/static/gambar', foto_fn)
    ubah_size=(300,300)
    j=Image.open(form_gmbr)
    j.thumbnail(ubah_size)
    j.save(foto_path)
    #form_foto.save(foto_path)
    return foto_fn

#### surat Skl #########
#def simpan_skl(form_surat_lls):
    random_hex= secrets.token_hex(8)
    f_name, f_ext= os.path.splitext(form_surat_lls.filename)
    foto_fn= random_hex + f_ext
    foto_path= os.path.join(app.root_path, 'albina/static/gambar', foto_fn)
    ubah_size=(300,300)
    j=Image.open(form_surat_lls)
    j.thumbnail(ubah_size)
    j.save(foto_path)
    #form_foto.save(foto_path)
    return foto_fn


######### Galeri ###########
@buser.route("/",  methods=['GET','POST'], defaults={"page": 1})
@buser.route("//<int:page>", methods=['GET', 'POST'])
def landing(page):
    page=page
    pages=4
    datagaleri=Dt_galeri.query.all()
    dataprogram=Dt_program.query.all()
    datakegiatan=Dt_kegiatan.query.all()
    databerita=Dt_berita.query.all()
    datagaleri = Dt_galeri.query.order_by(Dt_galeri.id.asc ()).paginate(page, pages, error_out=False)
    datasarana=Dt_sarana.query.all()
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datagaleri = Dt_galeri.query.filter(Dt_galeri.ket.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/galeri.html", datagaleri=datagaleri, form=form, tag=tag)
    return render_template ("user2/landing.html",datagaleri=datagaleri, dataprogram=dataprogram, datakegiatan=datakegiatan, databerita=databerita, datasarana=datasarana)

@buser.route("/homeeee/")
def home():
    return render_template ("user/home.html ")

@buser.route("/home")
def home1():
    return render_template ("user2/base.html ")


@buser.route("/profil/sekolah")
def profil():
    dataprofil=Dt_profil.query.all()
    return render_template ("user2/profil.html", dataprofil=dataprofil)


@buser.route("/galeri/sekolah",  methods=['GET','POST'], defaults={"page": 1})
@buser.route("/galeri/sekolah/<int:page>", methods=['GET', 'POST'])
def galeri(page):
    page=page
    pages=5
    datagaleri=Dt_galeri.query.all()
    datagaleri = Dt_galeri.query.order_by(Dt_galeri.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datagaleri = Dt_galeri.query.filter(Dt_galeri.ket.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/galeri.html", datagaleri=datagaleri, form=form, tag=tag)
    return render_template ("user2/galeri.html", datagaleri=datagaleri)


#### PROGRAM #######

@buser.route("/program/sekolah",  methods=['GET','POST'], defaults={"page": 1})
@buser.route("/program/sekolah/<int:page>", methods=['GET', 'POST'])
def program(page):
    page=page
    pages=5
    dataprogram=Dt_program.query.all()
    dataprogram = Dt_program.query.order_by(Dt_program.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        dataprogram = Dt_program.query.filter(Dt_program.ket.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/program.html", dataprogram=dataprogram, form=form, tag=tag)
    return render_template ("user2/program.html", dataprogram=dataprogram)


@buser.route("/kegiatan/sekolah",  methods=['GET','POST'], defaults={"page": 1})
@buser.route("/kegiatan/sekolah/<int:page>", methods=['GET', 'POST'])
def kegiatan(page):
    page=page
    pages=5
    datakegiatan=Dt_kegiatan.query.all()
    datakegiatan = Dt_kegiatan.query.order_by(Dt_kegiatan.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datakegiatan = Dt_kegiatan.query.filter(Dt_kegiatan.ket.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/kegiatan.html", datakegiatan=datakegiatan, form=form, tag=tag)
    return render_template ("user2/kegiatan.html", datakegiatan=datakegiatan)



@buser.route("/berita/sekolah",  methods=['GET','POST'], defaults={"page": 1})
@buser.route("/berita/sekolah/<int:page>", methods=['GET', 'POST'])
def berita(page):
    page=page
    pages=5
    databerita=Dt_berita.query.all()
    databerita = Dt_berita.query.order_by(Dt_berita.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        databerita = Dt_berita.query.filter(Dt_berita.ket.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/berita.html", databerita=databerita, form=form, tag=tag)
    return render_template ("user2/berita.html", databerita=databerita)

@buser.route("/sarana/sekolah",  methods=['GET','POST'], defaults={"page": 1})
@buser.route("/sarana/sekolah/<int:page>", methods=['GET', 'POST'])
def sarana(page):
    page=page
    pages=5
    datasarana=Dt_sarana.query.all()
    datasarana = Dt_sarana.query.order_by(Dt_sarana.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datasarana = Dt_sarana.query.filter(Dt_sarana.ket.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/sarana.html", datasarana=datasarana, form=form, tag=tag)
    return render_template ("user2/sarana.html", datasarana=datasarana)


#### pendaftaran siswa


@buser.route("/login-siswa", methods=['GET','POST'])
def login_siswa1():
    if current_user.is_authenticated:
        return redirect(url_for('buser.landing'))
    form=login_siswa()
    if form.validate_on_submit():
        cekniss=Dt_daftar.query.filter_by(niss=form.niss.data).first()
        if cekniss and bcrypt.check_password_hash(cekniss.password, form.password.data):
            login_user(cekniss)
            flash('selamat Datang Kembali !!')
            return redirect(url_for('buser.login_siswa1'))
        else:
            flash('login gagal')
    return render_template("user2/login_siswa.html", form=form)

@buser.route("/akun/siswa")
@login_required
def akun_siswa():
    return render_template("user2/akunsiswa.html ")

@buser.route("/pendaftaran/cek-status")
@login_required
def cek():
    return render_template("user2/cek.html ")



@buser.route("/daftar-siswa", methods=['GET','POST'])
def daftar_s():
    form=daftar_siswa()
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        datasiswa= Dt_daftar(niss=form.niss.data, nm_siswa=form.nm_siswa.data, tmpt_lhr=form.tmpt_lhr.data, tgl_lhr=form.tgl_lhr.data, jk=form.jk.data, almt_siswa=form.almt_siswa.data, agama=form.agama.data,  nm_ortu=form.nm_ortu.data, telp_ortu=form.telp_ortu.data, password=pass_hash, gmbr=file_gambar)
        db.session.add(datasiswa)
        db.session.commit()
        flash('Terimakasih Telah Melakukan Pendaftaran Siswa','primary')
        return redirect(url_for('buser.login_siswa1'))
    return render_template("user2/pendaftaran.html ", form=form)


@buser.route("/update-siswa", methods=['GET', 'POST'])
@login_required
def update_siswa():
    form=updt_siswa()  
    if form.validate_on_submit():
        if form.gmbr.data:
            file_foto=simpan_gambar(form.gmbr.data)
            current_user.gmbr= file_foto
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        current_user.niss=form.niss.data
        current_user.nm_siswa=form.nm_siswa.data
        current_user.tmpt_lhr =form.tmpt_lhr.data
        current_user.tgl_lhr=form.tgl_lhr.data
        current_user.jk=form.jk.data
        current_user.almt_siswa=form.almt_siswa.data  
        current_user.agama=form.agama.data
        current_user.nm_ortu=form.nm_ortu.data
        current_user.telp_ortu=form.telp_ortu.data
        current_user.password=pass_hash
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('buser.update_siswa'))  
    elif request.method=="GET":
        form.niss.data=current_user.niss
        form.nm_siswa.data=current_user.nm_siswa
        form.tmpt_lhr.data=current_user.tmpt_lhr
        form.tgl_lhr.data=current_user.tgl_lhr
        form.jk.data=current_user.jk   
        form.almt_siswa.data=current_user.almt_siswa
        form.agama.data=current_user.agama
        form.nm_ortu.data=current_user.nm_ortu
        form.telp_ortu.data=current_user.telp_ortu
        form.password.data=current_user.password
    return render_template('user2/updatesiswa.html', form=form)

#@buser.route('/', methods=[' GET', 'POST'])
#def up():
    form = Dt_daftar()
    if request.method== "POST":
        if form.validate_on_submit():
            file_name= form.surat_lls.data



@buser.route("/logout-akun")
def logout_siswa():  
    logout_user()
    return redirect(url_for('buser.landing'))
