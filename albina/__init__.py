from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_ckeditor import CKEditor

# konfirgurasis #
app=Flask('__name__', template_folder='albina/templates', static_folder='albina/static')

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///webalbina.db'
db=SQLAlchemy(app)
app.config['SECRET_KEY']="smpitalbina"

db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_menager=LoginManager(app)
ckeditor = CKEditor(app)


#registrasi blueprint #
from albina.admin.routes import badmin
app.register_blueprint(badmin)

from albina.user.routes import buser
app.register_blueprint(buser)

