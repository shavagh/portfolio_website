import os

# set flask app configuration
class Config:
    SECRET_KEY = 'b5034ef2e3c20f02ebcb002d' # set secret key for validation
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db' # path to database 
    MAIL_SERVER = 'smtp.gmail.com' # use gmail server to send email
    MAIL_PORT = 587 # port number
    MAIL_USE_TLS = True # encrypt data when send message
    MAIL_USERNAME = os.environ.get('EMAIL_USER') # email enviromental variables
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS') # email password enviromental variables