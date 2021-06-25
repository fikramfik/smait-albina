from flask.helpers import get_template_attribute
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from albina.dtbase import Dt_admin, Dt_daftar
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_ckeditor import CKEditorField

############## form admin ###########
#daftar akun admin
class dftr_fadmin(FlaskForm):
    nip= StringField('NIP',validators=[DataRequired()])
    nama= StringField('Nama Lengkap',validators=[DataRequired()])
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    password= PasswordField('Password',validators=[DataRequired(), Length(min=5, max=15)])
    konf_pass= PasswordField('Konfirmasi Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Daftar')

    def validate_nip(self,nip):
        ceknip=Dt_admin.query.filter_by(nip=nip.data).first()
        if ceknip:
            raise ValidationError('NIP Telah Digunakan!')

#login admin
class login_fadmin(FlaskForm):
    nip= StringField('NIP',validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired(), Length(min=6, max=15)])
    submit= SubmitField('Masuk')
    


# ubah password
class updt_fadmin(FlaskForm):
    nip= StringField('Username',validators=[DataRequired()])
    nama= StringField('Nama Lengkap',validators=[DataRequired()])
    password= PasswordField('Password Baru',validators=[DataRequired()])
    konf_pass= PasswordField('Konfirmasi Password',validators=[DataRequired(), EqualTo('password')])
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpeg','jpg','png'])])
    submit= SubmitField('ubah')
    
    def validate_nip(self,nip):
        if nip.data !=current_user.nip:
            ceknip=Dt_admin.query.filter_by(nip=nip.data).first()
            if ceknip:
                raise ValidationError('Maaf, username yang anda masukannn salah!')

################# form siswa #################

class dt_fdaftar(FlaskForm):
    iss= StringField('NISS',validators=[DataRequired()])
    nm_siswa= StringField('Nama Lengkap',validators=[DataRequired()])
    tmpt_lhr= StringField('Tempat Lahir',validators=[DataRequired()])
    tgl_lhr= StringField('Tanggal Lahir',validators=[DataRequired()])
    jk= SelectField('Jenis Kelamin', choices=[('Perempuan','Perempuan'),('Laki-Laki','Laki-Laki')],validators=[DataRequired()])
    almt_siswa= StringField('Alamat Tinggal',validators=[DataRequired()])
    agama= StringField('Agama',validators=[DataRequired()])
    nm_ortu= StringField('Nama Orang Tua/Wali',validators=[DataRequired()])
    telp_ortu= StringField('No.Telp',validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired()])
    gmbr=FileField('Surat Lulus',validators=[FileAllowed(['jpg','jpeg','png', 'pdf'])])
    submit= SubmitField('Tambah Data')

    def validate_niss(self,niss):
        cekniss=Dt_daftar.query.filter_by(niss=niss.data).first()
        if cekniss:
            raise ValidationError('Maaf, NISS Anda Sudah digunakan!')


############### form profil ################
# tamba data profil
class dt_fprofil(FlaskForm):
    profil= CKEditorField('Profil Sekolah',validators=[DataRequired()])
    visi= CKEditorField('Visi',validators=[DataRequired()])
    misi= CKEditorField('Misi',validators=[DataRequired()])
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    submit= SubmitField('Tambah Data')

# ubah data profil
class upt_profil(FlaskForm):
    profil= CKEditorField('Profil Sekolah',validators=[DataRequired()])
    visi= CKEditorField('Visi',validators=[DataRequired()])
    misi= CKEditorField('Misi',validators=[DataRequired()])
    gmbr=FileField('Ubah Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    submit= SubmitField('Ubah Data')
    
############### form galeri ################
# tamba data galeri
class dt_fgaleri(FlaskForm):
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Tambah Data')

# ubah data galeri
class upt_galeri(FlaskForm):
    gmbr=FileField('Ubah Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Ubah Data')

############### form sarana ################
# tamba data sarana
class dt_fsarana(FlaskForm):
    sarana= StringField('Sarana-Prasarana',validators=[DataRequired()])
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Tambah Data')

# ubah data sarana
class upt_sarana(FlaskForm):
    sarana= StringField('Sarana-Prasarana',validators=[DataRequired()])
    gmbr=FileField('Ubah Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Ubah Data')

############### form program ################
# tamba data program
class dt_fprogram(FlaskForm):
    program= StringField('Nama Program',validators=[DataRequired()]) 
    gmbr=FileField(' Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Tambah Data')

# ubah data program
class upt_program(FlaskForm):
    program= StringField('Nama Program',validators=[DataRequired()])
    gmbr=FileField('Ubah Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Ubah Data')

############### form kegiatan ################
# tamba data kegiatan
class dt_fkegiatan(FlaskForm):
    kegiatan= StringField('Nama kegiatan',validators=[DataRequired()]) 
    gmbr=FileField(' Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Tambah Data')

# ubah data kegiatan
class upt_kegiatan(FlaskForm):
    kegiatan= StringField('Nama kegiatan',validators=[DataRequired()])
    gmbr=FileField('Ubah Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Ubah Data')

############### form berita ################
# tamba data berita
class dt_fberita(FlaskForm):
    berita= StringField('Nama Berita',validators=[DataRequired()]) 
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Tambah Data')

# ubah data berita
class upt_berita(FlaskForm):
    berita= StringField('Nama Berita',validators=[DataRequired()])
    gmbr=FileField('Ubah Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
    submit= SubmitField('Ubah Data')






