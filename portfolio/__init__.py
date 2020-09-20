from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from portfolio.config import Config


db = SQLAlchemy() # initialise SQL database extention
bcrypt = Bcrypt() # initialise Bcrypt encryption extention
login_manager = LoginManager() # initialise Login Manager extention
login_manager.login_view = 'users.login' # assign login view page 
login_manager.login_message_category = 'info' # assign message category
mail = Mail() # initialise Mail extention

# initialise app configuration and blueprints 
def create_app(config_class=Config): # set configuration
    app = Flask(__name__) # initialise Flask 
    app.config.from_object(Config) # set configuration from config parameter object
    db.init_app(app) # initialise database to flask app
    bcrypt.init_app(app) # initialise bcrypt encryption to flask app
    login_manager.init_app(app)  # initialise login manager to flask app
    mail.init_app(app)  # initialise mail to flask app

    # import blueprints created in files
    from portfolio.users.routes import users
    from portfolio.posts.routes import posts
    from portfolio.main.routes import main
    from portfolio.errors.handlers import errors    
    
    # add blueprints to flask app
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    # return completed application
    return app