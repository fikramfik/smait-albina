from flask.app import Flask
from flask.helpers import get_template_attribute
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo
from albina.dtbase import Dt_daftar
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user

############### form profil ################
# tamba data profil
class dt_fprofil(FlaskForm):
    profil= TextAreaField('Profil Sekolah',validators=[DataRequired()])
    visi= TextAreaField('Visi',validators=[DataRequired()])
    misi= TextAreaField('Misi',validators=[DataRequired()])
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    
    
############### form galeri ################
# tamba data galeri
class dt_fgaleri(FlaskForm):
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
 
############### form sarana ################
# tamba data sarana
class dt_fsarana(FlaskForm):
    sarana= StringField('Keterangan',validators=[DataRequired()])
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])
 


class dt_fprogram(FlaskForm):
    program= StringField('Nama Program',validators=[DataRequired()]) 
    gmbr=FileField(' Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])


############### form kegiatan ################
# tamba data kegiatan
class dt_fkegiatan(FlaskForm):
    kegiatan= StringField('Nama kegiatan',validators=[DataRequired()]) 
    gmbr=FileField(' Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])

############### form berita ################
# tamba data berita
class dt_fberita(FlaskForm):
    berita= StringField('Nama Berita',validators=[DataRequired()]) 
    gmbr=FileField('Gambar',validators=[FileAllowed(['jpg','jpeg','png'])])
    ket= StringField('Keterangan',validators=[DataRequired()])

################### Bagian Siswa #####################

class dt_fakun(FlaskForm):
    niss= StringField('NISS',validators=[DataRequired()])
    username= StringField('Username',validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired()])
    konf_pass= PasswordField('Konfirmasi Password',validators=[DataRequired(), EqualTo('password')])
    submit= SubmitField('Daftar')

    def validate_niss(self,niss):
        cekniss=Dt_daftar.query.filter_by(niss=niss.data).first()
        if cekniss:
            raise ValidationError('Maaf, NISS yang Anda Masukkan Sudah Terdaftar!')

class login_siswa(FlaskForm):
    niss= StringField('NISS',validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired()])
    submit= SubmitField('Login')

    

class daftar_siswa(FlaskForm):
    niss= StringField('NISS',validators=[DataRequired(),Length(min=5, max=20)])
    nm_siswa= StringField('Nama Lengkap',validators=[DataRequired()])
    tmpt_lhr= StringField('Tempat Lahir',validators=[DataRequired()])
    tgl_lhr= StringField('Tanggal Lahir',validators=[DataRequired()])
    jk= SelectField('Jenis Kelamin', choices=[('Perempuan','Perempuan'),('Laki-Laki','Laki-Laki')],validators=[DataRequired()])
    almt_siswa= StringField('Alamat',validators=[DataRequired()])
    agama= StringField('Agama',validators=[DataRequired()])
    nm_ortu= StringField('Nama Orang Tua/wali',validators=[DataRequired()])
    telp_ortu= StringField('No Telpon Orang Tua',validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired(),Length(min=5, max=15)])
    gmbr=FileField('Surat Lulus',validators=[FileAllowed(['jpg','jpeg','png','pdf'])])
    submit= SubmitField('Daftar')

    def validate_niss(self,niss):
        ccekniss=Dt_daftar.query.filter_by(niss=niss.data).first()
        if ccekniss:
            raise ValidationError('Maaf, NISS yang anda masukkan telah terdaftar!')


class updt_siswa(FlaskForm):
    niss= StringField('NISS',validators=[DataRequired(),Length(min=5, max=20)])
    nm_siswa= StringField('Nama Lengkap',validators=[DataRequired()])
    tmpt_lhr= StringField('Tempat Lahir',validators=[DataRequired()])
    tgl_lhr= StringField('Tanggal Lahir',validators=[DataRequired()])
    jk= SelectField('Jenis Kelamin', choices=[('Perempuan','Perempuan'),('Laki-Laki','Laki-Laki')],validators=[DataRequired()])
    almt_siswa= StringField('Alamat',validators=[DataRequired()])
    agama= StringField('Agama',validators=[DataRequired()])
    nm_ortu= StringField('Nama Orang Tua',validators=[DataRequired()])
    telp_ortu= StringField('No Telpon Orang Tua',validators=[DataRequired()])
    password= PasswordField('Password',validators=[DataRequired()])
    konf_pass= PasswordField('Konfirmasi Password',validators=[DataRequired(), EqualTo('password')])
    gmbr=FileField('Surat Lulus',validators=[FileAllowed(['jpg','jpeg','png', 'pdf'])])
    submit= SubmitField('ubah')

    def validate_niss(self,niss):
        if niss.data !=current_user.niss:
            cekniss=Dt_daftar.query.filter_by(niss=niss.data).first()
            if cekniss:
                raise ValidationError('Maaf, Niss sudah digunakan!')
