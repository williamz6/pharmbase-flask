# app/__init__.py
import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flaskext.mysql import MySQL
import pymysql

from flask_paginate import Pagination, get_page_parameter


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pharmbase.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey'
app.config['WTF_CSRF_ENABLED']= True


db = SQLAlchemy(app)
csrf = CSRFProtect(app)
login_manager= LoginManager(app)

login_manager.login_message = "You are not authorised to see this page. Please log in"
login_manager.login_view = "auth.login"


bcrypt = Bcrypt(app)


Bootstrap(app)

migrate = Migrate(app, db)


from pharmbase import models

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint, url_prefix='/admin')

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)



