#Here, we initial the web application and load up
#All the different components we intend to use

import os
#Attemp 2 at making a simple Flask Blog
#url_for can be used to find files without knowing their exact directory location
from flask import Flask
#What does url_for actually do?!
#How do I style my websie. GOOD FREEKIG LORD WHY DOES THE STYLESHEET NOT CHANGE WHEN I CHANGE IT
#SQLite can be used for development, whilte
#SQLsomething can be used for the live version
#Flask-Alchemy allows us to communicate with any type of database without having to change any code
from flask_sqlalchemy import SQLAlchemy
#This module allows us to encrypt passwords to protect the users on the site
from flask_bcrypt import Bcrypt
#Flask has an extension for managing logins
from flask_login import LoginManager
#For sending mail
from flask_mail import Mail
from flaskblog.config import BaseConfig

#Database instance
#Database structure created through the use of models
#Each model class will be a single table in the database
db = SQLAlchemy()

#Initialising Bcrypt
bcrypt = Bcrypt()

#Flask's login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

#This is our base app setup, using a configuration we specified in the config.py folder
def create_app(config_class=BaseConfig):
	app = Flask(__name__)
	app.config.from_object(config.ProductionConfig)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main
	from flaskblog.errors.handlers import errors
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	app.register_blueprint(errors)

	return app