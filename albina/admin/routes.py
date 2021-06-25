
from flask import Flask, Blueprint,flash, render_template, url_for, redirect, request
from albina import db, bcrypt
from albina import app
from flask_wtf import file
from wtforms import form
from wtforms.validators import DataRequired
from albina.dtbase import Dt_daftar,Dt_admin, Dt_profil,Dt_berita,Dt_program,Dt_kegiatan,Dt_galeri,Dt_sarana# Tabel bagian database
from albina.admin.forms import updt_fadmin,dt_fberita, dt_fgaleri,dt_fkegiatan, dt_fprofil,dt_fprogram, login_fadmin,upt_berita,upt_profil,upt_kegiatan,upt_galeri,upt_program,upt_sarana, dt_fsarana, dt_fdaftar , dftr_fadmin # data dari forms
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import os
import secrets

badmin= Blueprint('badmin',__name__)

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

#simpan surat


@badmin.route("/dashboard", methods=['GET','POST'])
def dasboard():
    return render_template("admin/dashboard.html")

@badmin.route("/jalan-tikus-jangan-lewat", methods=['GET','POST'])
def akun():
    form=dftr_fadmin()
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        dataadmin=Dt_admin(nip=form.nip.data, password=pass_hash, nama=form.nama.data, gmbr=file_gambar)
        db.session.add(dataadmin)
        db.session.commit()
        return redirect(url_for('badmin.dasboard'))
    return render_template("admin/akun.html", form=form)

 
@badmin.route("/data-admin", methods=['GET','POST'])
def admin(): 
    form=dftr_fadmin()
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        dataadmin=Dt_admin(nip=form.nip.data, password=pass_hash, nama=form.nama.data, gmbr=file_gambar)
        db.session.add(dataadmin)
        db.session.commit()
        return redirect(url_for('badmin.dasboard'))
    return render_template("admin/admin.html", form=form)


@badmin.route("/login-admin", methods=['GET','POST'])
def login_admin():
    if current_user.is_authenticated:
        return redirect(url_for('badmin.dasboard'))
    form=login_fadmin()
    if form.validate_on_submit():
        ceknip=Dt_admin.query.filter_by(nip=form.nip.data).first()
        if ceknip and bcrypt.check_password_hash(ceknip.password, form.password.data):
            login_user(ceknip)
            flash('Anda Berhasil Login!')
            return redirect(url_for('badmin.login_admin'))
        else:
            flash('login gagal')
    return render_template("admin/login.html",form=form)


@badmin.route("/update-admin", methods=['GET', 'POST'])
def update_admin():
    form=updt_fadmin() 
    if form.validate_on_submit():
        if form.gmbr.data:
            file_gambar=simpan_gambar(form.gmbr.data)
            current_user.foto = file_gambar
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        current_user.nip=form.nip.data
        current_user.nama=form.nama.data
        current_user.password=pass_hash
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('badmin.dasboard'))
    elif request.method=="GET":
        form.nip.data= current_user.nip
        form.nama.data=current_user.nama
        form.password.data=current_user.password
    return render_template('admin/uptadmin.html', form=form)

@badmin.route("/akun-admin")
@login_required
def akunadmin():
    return render_template("admin/akunadmin.html")


############ profile sekolah #############

@badmin.route("/profil-sekolah",  methods=['GET','POST'])
def profil():
    form=dt_fprofil()
    dataprofil=Dt_profil.query.all()
    if form.validate_on_submit():
        add= Dt_profil(profil=form.profil.data, visi=form.visi.data, misi=form.misi.data)
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di Tambah','primary')
        return redirect(url_for('badmin.profil'))
    return render_template ("admin/profil.html", dataprofil=dataprofil,  form=form)


@badmin.route("/update-profil/<int:ed_id>/update", methods=['GET', 'POST'])
def update_profil(ed_id):
    dataprofil=Dt_profil.query.get_or_404(ed_id)
    form=upt_profil()
    if form.validate_on_submit():
        dataprofil.profil=form.profil.data
        dataprofil.visi=form.visi.data
        dataprofil.misi=form.misi.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('badmin.profil'))
    elif request.method=="GET":
        form.profil.data=dataprofil.profil
        form.visi.data=dataprofil.visi
        form.misi.data=dataprofil.misi
    return render_template('admin/uptprofil.html', form=form)

@badmin.route("/hapus-profil/<id>", methods=['GET', 'POST'])
def hapus_profil(id):
    qprofil=Dt_profil.query.get(id)
    db.session.delete(qprofil)
    db.session.commit()
    return redirect(url_for('badmin.berita'))
###############################################

###### program sekolah #################

@badmin.route("/program-sekolah",  methods=['GET','POST'], defaults={"page": 1})
@badmin.route("/program-sekolah/<int:page>", methods=['GET', 'POST'])

def program(page):
    page=page
    pages=2
    form=dt_fprogram()
    dataprogram=Dt_program.query.all()
    dataprogram = Dt_program.query.order_by(Dt_program.id.asc()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        dataprogram = Dt_program.query.filter(Dt_program.program.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/program.html", dataprogram=dataprogram, form=form, tag=tag)
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        add= Dt_program(program=form.program.data,ket=form.ket.data, gmbr=file_gambar)
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di Tambah','primary')
        return redirect(url_for('badmin.program'))
    return render_template ("admin/program.html", dataprogram=dataprogram,  form=form)

@badmin.route("/update-program/<int:ed_id>/update", methods=['GET', 'POST'])
def update_program(ed_id):
    dataprogram=Dt_program.query.get_or_404(ed_id)
    form=upt_program()
    if form.validate_on_submit():
        if form.gmbr.data:
            file_gambar=simpan_gambar(form.gmbr.data)
            form.foto = file_gambar
        dataprogram.program=form.program.data
        dataprogram.gmbr=file_gambar
        dataprogram.ket=form.ket.data
        db.session.commit()
        return redirect(url_for('badmin.program'))
    elif request.method=="GET":
        form.program.data=dataprogram.program
        form.ket.data=dataprogram.ket
    return render_template('admin/uptprogram.html', form=form)

@badmin.route("/hapus-program/<id>", methods=['GET', 'POST'])
def hapus_program(id):
    qprogram=Dt_program.query.get(id)
    db.session.delete(qprogram)
    db.session.commit()
    return redirect(url_for('badmin.program')) 
############################################

############## kegiatan siswa ####################

@badmin.route("/kegiatan-sekolah",  methods=['GET','POST'], defaults={"page": 1})
@badmin.route("/kegiatan-sekolah/<int:page>", methods=['GET', 'POST'])
def kegiatan(page):
    page=page
    pages=2
    form=dt_fkegiatan()
    datakegiatan=Dt_kegiatan.query.all()
    datakegiatan = Dt_kegiatan.query.order_by(Dt_kegiatan.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datakegiatan = Dt_kegiatan.query.filter(Dt_kegiatan.kegiatan.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/kegiatan.html", datakegiatan=datakegiatan, form=form, tag=tag)
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        add= Dt_kegiatan(kegiatan=form.kegiatan.data,ket=form.ket.data, gmbr=file_gambar)
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di Tambah','primary')
        return redirect(url_for('badmin.kegiatan'))
    return render_template ("admin/kegiatan.html", datakegiatan=datakegiatan,  form=form)


@badmin.route("/update-kegiatan/<int:ed_id>/update", methods=['GET', 'POST'])
def update_kegiatan(ed_id):
    datakegiatan=Dt_kegiatan.query.get_or_404(ed_id)
    form=upt_kegiatan()
    if form.validate_on_submit():
        if form.gmbr.data:
            file_gambar=simpan_gambar(form.gmbr.data)
            form.foto = file_gambar
        datakegiatan.kegiatan=form.kegiatan.data
        datakegiatan.gmbr=file_gambar
        datakegiatan.ket=form.ket.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('badmin.kegiatan'))
    elif request.method=="GET":
        form.kegiatan.data=datakegiatan.kegiatan
        form.ket.data=datakegiatan.ket
    return render_template('admin/uptkegiatan.html', form=form)

@badmin.route("/hapus-kegiatan/<id>", methods=['GET', 'POST'])
def hapus_kegiatan(id):
    qkegiatan=Dt_kegiatan.query.get(id)
    db.session.delete(qkegiatan)
    db.session.commit()
    return redirect(url_for('badmin.profil'))
##############################################

############# Sarana Prasarana ############

@badmin.route("/sarana-sekolah",  methods=['GET','POST'], defaults={"page": 1})
@badmin.route("/sarana-sekolah/<int:page>", methods=['GET', 'POST'])
@login_required
def sarana(page):
    page=page
    pages=2
    form=dt_fsarana()
    datasarana=Dt_sarana.query.all()
    datasarana = Dt_sarana.query.order_by(Dt_sarana.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datasarana = Dt_sarana.query.filter(Dt_sarana.sarana.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/sarana.html", datasarana=datasarana, form=form, tag=tag)
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        add= Dt_sarana(sarana=form.sarana.data,ket=form.ket.data, gmbr=file_gambar)
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di Tambah','primary')
        return redirect(url_for('badmin.sarana'))
    return render_template ("admin/sarana.html", datasarana=datasarana,  form=form)
    
@badmin.route("/update-sarana/<int:ed_id>/update", methods=['GET', 'POST'])
def update_sarana(ed_id):
    datasarana=Dt_sarana.query.get_or_404(ed_id)
    form=upt_sarana()
    if form.validate_on_submit():
        if form.gmbr.data:
            file_gambar=simpan_gambar(form.gmbr.data)
            form.foto = file_gambar
        datasarana.sarana=form.sarana.data
        datasarana.ket=form.ket.data
        datasarana.gmbr=file_gambar
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('badmin.sarana'))
    elif request.method=="GET":
        form.sarana.data=datasarana.sarana
        form.ket.data=datasarana.ket
    return render_template('admin/uptsarana.html', form=form)

@badmin.route("/hapus-sarana/<id>", methods=['GET', 'POST'])
def hapus_sarana(id):
    qsarana=Dt_sarana.query.get(id)
    db.session.delete(qsarana)
    db.session.commit()
    return redirect(url_for('badmin.sarana'))


########### Berita ##############
@badmin.route("/berita-sekolah",  methods=['GET','POST'], defaults={"page": 1})
@badmin.route("/berita-sekolah/<int:page>", methods=['GET', 'POST'])
@login_required
def berita(page):
    page=page
    pages=2
    form=dt_fberita()
    databerita=Dt_berita.query.all()
    databerita = Dt_berita.query.order_by(Dt_berita.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        databerita = Dt_berita.query.filter(Dt_berita.berita.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/berita.html", databerita=databerita, form=form, tag=tag)
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        add= Dt_berita(berita=form.berita.data,ket=form.ket.data, gmbr=file_gambar)
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di Tambah','primary')
        return redirect(url_for('badmin.berita'))
    return render_template ("admin/berita.html", databerita=databerita,  form=form)

@badmin.route("/profil-admin")
def profiladmin():
    dataadmin=Dt_admin.query.all()
    return render_template ("admin/dtladmin.html", dataadmin=dataadmin)

@badmin.route("/update-berita/<int:ed_id>/update", methods=['GET', 'POST'])
def update_berita(ed_id):
    databerita=Dt_berita.query.get_or_404(ed_id)
    form=upt_berita()
    if form.validate_on_submit():
        if form.gmbr.data:
            file_gambar=simpan_gambar(form.gmbr.data)
            form.foto = file_gambar
        databerita.berita=form.berita.data
        databerita.ket=form.ket.data
        databerita.gmbr=file_gambar
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('badmin.berita'))
    elif request.method=="GET":
        form.berita.data=databerita.berita
        form.ket.data=databerita.ket
    return render_template('admin/uptberita.html', form=form)

@badmin.route("/hapus-berita/<id>", methods=['GET', 'POST'])
def hapus_berita(id):
    qberita=Dt_berita.query.get(id)
    db.session.delete(qberita)
    db.session.commit()
    return redirect(url_for('badmin.berita'))




######### Galeri ###########
@badmin.route("/galeri-sekolah",  methods=['GET','POST'], defaults={"page": 1})
@badmin.route("/galeri-sekolah/<int:page>", methods=['GET', 'POST'])
def galeri(page):
    page=page
    pages=2
    form=dt_fgaleri()
    datagaleri=Dt_galeri.query.all()
    datagaleri = Dt_galeri.query.order_by(Dt_galeri.id.asc ()).paginate(page, pages, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datagaleri = Dt_galeri.query.filter(Dt_galeri.ket.like(search)).paginate(page, pages, error_out=False)
        return render_template("admin/galeri.html", datagaleri=datagaleri, form=form, tag=tag)
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        add= Dt_galeri(ket=form.ket.data, gmbr=file_gambar)
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di Tambah','primary')
        return redirect(url_for('badmin.galeri'))
    return render_template ("admin/galeri.html", datagaleri=datagaleri,  form=form)


@badmin.route("/update-galeri/<int:ed_id>/update", methods=['GET', 'POST'])
def update_galeri(ed_id):
    datagaleri=Dt_galeri.query.get_or_404(ed_id)
    form=upt_galeri()
    if form.validate_on_submit():
        if form.gmbr.data:
            file_gambar=simpan_gambar(form.gmbr.data)
            form.foto = file_gambar
        datagaleri.gmbr=file_gambar
        datagaleri.ket=form.ket.data
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('badmin.galeri'))
    elif request.method=="GET":
        form.ket.data=datagaleri.ket
    return render_template('admin/uptgaleri.html', form=form)

@badmin.route("/hapus-galeri/<id>", methods=['GET', 'POST'])
def hapus_galeri(id):
    qgaleri=Dt_galeri.query.get(id)
    db.session.delete(qgaleri)
    db.session.commit()
    return redirect(url_for('badmin.galeri'))


####################



##### pendaftaran siswa  lewat admin ##########
@badmin.route("/data/siswa-baru",  methods=['GET','POST'], defaults={"hal": 1})
@badmin.route("/<int:hal>", methods=['GET', 'POST'])
def siswa1(hal):
    hal=hal
    hals=10
    form=dt_fdaftar()
    datasiswa=Dt_daftar.query.all()
    datasiswa = Dt_daftar.query.order_by(Dt_daftar.id.asc ()).paginate(hal, hals, error_out=False)
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        datasiswa = Dt_daftar.query.filter(Dt_daftar.tag.like(search)).paginate(hal, hals, error_out=False)
        return render_template("admin/siswabaru.html", datasiswa=datasiswa, tag=tag)
    if form.validate_on_submit():
        file_gambar=simpan_gambar(form.gmbr.data)
        add= Dt_daftar(niss=form.niss.data, nm_siswa=form.nm_siswa.data, tmpt_lhr =form.tmpt_lhr.data, tgl_lhr=form.tgl_lhr.data, jk=form.jk.data,  almt_siswa=form.almt_siswa.data, agama=form.agama.data, nm_ortu=form.nm_ortu.data, telp_ortu=form.telp_ortu.data,password=form.password.data,  gmbr=file_gambar  )
        db.session.add(add)
        db.session.commit()
        flash('Data Berhasil Di Tambah','primary')
        return redirect(url_for('badmin.siswa1'))
    return render_template ("admin/siswabaru.html", datasiswa=datasiswa,  form=form)

#@badmin.route("/update-siswa/<int:ed_id>/update", methods=['GET', 'POST'])
#def update_siswa(ed_id):
    datasiswa=Dt_daftar.query.get_or_404(ed_id)
    form=upt_siswa()
    if form.validate_on_submit():
        if form.gmbr.data:
            file_gambar=simpan_gambar(form.gmbr.data)
            form.foto = file_gambar
        pass_hash=bcrypt.generate_password_hash(form.password.data).decode('UTF-8')
        datasiswa.niss=form.niss
        datasiswa.nm_siswa=form.nm_siswa
        datasiswa.tmpt_lhr =form.tmpt_lhr 
        datasiswa.tgl_lhr=form.tgl_lhr
        datasiswa.almt_siswa=form.almt_siswa
        datasiswa.agama=form.agama
        datasiswa.nm_ortu=form.nm_ortu
        datasiswa.telp_ortu=form.telp_ortu
        datasiswa.password=pass_hash
        datasiswa.gmbr=file_gambar
        db.session.commit()
        flash('Data Berhasil Di ubah','warning')
        return redirect(url_for('badmin.siswa'))
    #elif request.method=="GET":
        form.niss=datasiswa.niss
        form.nm_siswa=datasiswa.nm_siswa
        form.tmpt_lhr=datasiswa.tmpt_lhr  
        form.tgl_lhr=datasiswa.tgl_lhr
        form.jk=datasiswa.jk
        form.almt_siswa=datasiswa.almt_siswa
        form.agama=datasiswa.agama
        form.nm_ortu=datasiswa.nm_ortu
        form.telp_ortu=datasiswa.telp_ortu
        form.password.data=current_user.password
    #return render_template('admin/uptsiswa.html', form=form)


@badmin.route("/hapus-siswa/<id>", methods=['GET', 'POST'])
def hapus_siswa(id):
    qsiswa=Dt_daftar.query.get(id)
    db.session.delete(qsiswa)
    db.session.commit()
    return redirect(url_for('badmin.siswa')) 

@badmin.route("/logout-admin")
def logoutadmin():  
    logout_user()
    return redirect(url_for('badmin.login_admin'))


 





