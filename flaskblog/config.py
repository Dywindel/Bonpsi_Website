#This is the parent configuring file that will be accessed by different children
#Depending on which environment we're working in
import os

class BaseConfig(object):
	#He has moved this variables into os.environ variables during tutorial 11
	#I'm skipping this section because I don't want to worry about this yet
	#It's about halfway through the video
	DEBUG = False
	#Will add config file later on
	SECRET_KEY = 'bRv\xcd\x89\t\x10Jv\xeci#\x01nqsV\x8d$\r\xe5\x12\xe3\xcfo'
	#The /// sepcifies a relative path
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
	#For sending email
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	#These variables are stored privately in the windows environment variables list
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')

#Developement configuration for alternative envrionment
#In this case, debut mode
class DevelopmentConfig(BaseConfig):
	#We're overriding the debug mode in the BaseConfig
	DEBUG = True

#Tutorial creates a class for Heroku setup

#Final production setup
class ProductionConfig(BaseConfig):
	#We just want to be safe that in the live version that debug mode is off
	DEBUG = False