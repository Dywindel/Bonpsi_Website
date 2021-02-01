#Python date and time module
from datetime import datetime
#This file contains the class models used by the database
from flaskblog import db, login_manager
from flask import current_app
#?
from flask_login import UserMixin
#This import is used to create a secret key that expires after a certain time
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

#What is this doing?
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#Create a user model class database
class User(db.Model, UserMixin):
	#Each user gets an id number
	id = db.Column(db.Integer, primary_key=True)
	#Each username is unique and is limited to 'Max' characters atribute
	username = db.Column(db.String(20), unique=True, nullable=False)
	#Email
	email = db.Column(db.String(120), unique=True, nullable=False)
	#Image file that starts with a default image
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	#Password
	password = db.Column(db.String(60), nullable=False)
	#This data records all the posts a particular user has made
	#Backref allows a post to access the user who created the post
	#I don't understand lazy
	posts = db.relationship('Post', backref='author', lazy=True)

	#This method creates a timed token
	def get_reset_token(self, expires_secs=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_secs)
		#That says 's'-'dot'-'dump'-'s'
		return s.dumps({'user_id': self.id}).decode('utf-8')

	#This method verifies the token
	#This function _doesn't_ take self as an argument: it's a static method
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		#We put this in a try as the code may have expired when we try to validate it
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		#If we're successful, return the user_id
		return User.query.get(user_id)

	#This function controls how the object is printed when we print it out
	def __repr__(self):
		return f"User('{self.username}'), '{self.email}', '{self.image_file}')"

#Create a blog post class database
#We haven't included an author here as this will be achieved through a relationship
#With Post and User database
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	#Blogpost title
	title = db.Column(db.String(100), nullable=False)
	#Date of post, it a time wasn't specified, get the current time as default
	#For some reason, we're passing the 'utcnow' as a reference function, rather than the
	#Actual datetime 'utcnow()'
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	#Header image
	image_file = db.Column(db.String(20), nullable=True, default='default.png')
	#Text content of blog
	content = db.Column(db.Text, nullable=False)
	#The author of the post. Includes the primary key to help us recall the user who
	#Posted the content.
	#Certain references will switch to upper or lowercase for some reason
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}')"

#The basic interactions involved in communicating with the SQLAlchemy database are
#Create a database: db.create_all()
#Specify a user: user01 = M_User(username = 'name', email=...
#Same thing for a post: post01 = M_Post(title='Blog 1', content=...)
#Add the user: db.session.add(user01)
#Commit the changes: db.session.commit()
#Return all database M_Users: M_User.query.all()
#Or just the first user: M_User.query.first()
#Or filter names: M_User.query.filter_by(username='James').all()
#You can also delete everything: db.drop_all()