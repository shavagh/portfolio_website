from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__) # Flask constructor, takes the name of  current module (__name__) as argument. 
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245' # secret key for form protection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # create database at location 
db = SQLAlchemy(app) # initialise SQLAlchemy database 
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from portfolio import routes 