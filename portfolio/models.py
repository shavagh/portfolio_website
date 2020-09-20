from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from portfolio import db, login_manager
from flask_login import UserMixin

# load user's data from database
@login_manager.user_loader # load logged in user
def load_user(user_id): 
    return User.query.get(int(user_id)) # return user from database using user's id

# User database fields
class User(db.Model, UserMixin):
    # set database fields, data types and checks
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # create 1-many relationship (user can have many posts), with referencing author for both classes
    posts = db.relationship('Post', backref='author', lazy=True)

    # generate token to reset password
    def get_reset_token(self, expires_sec=1800):
        # creates token from secret key lasting for specified time 
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        # returns token id
        return s.dumps({'user_id': self.id}).decode('utf-8')

    # verifies user's token to reset password
    @staticmethod 
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY']) # store tokenized secret key
        try:
            user_id = s.loads(token)['user_id'] # gets token and matches it to user id in dictionary
        except:
            return None # return false
        return User.query.get(user_id) # return user

# Post database fields
class Post(db.Model):
    # set database fields, data types and checks
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # ser user id as foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 

