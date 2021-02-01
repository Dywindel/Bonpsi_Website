from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
#These validators are a class created by the wtforms add-on. They can restrict user input
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
#We'll need this for validation checks
from flaskblog.models import User

#Registration form
class RegistrationForm(FlaskForm):
	username = StringField('Username',
							validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
							validators=[DataRequired(), Email()])
	password = PasswordField('Password',
							validators=[DataRequired()])
	confirmpassword = PasswordField('Confirm Password',
							validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Submit')

	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('An account already exists with that email.')

#Login form
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	#A user ticked boolean if the user wants to be kept logged in
	remember = BooleanField('Remember Me')
	submit = SubmitField('login')

#Update account form
class UpdateAccountForm(FlaskForm):
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	def validate_username(self, username):
		#When a user changes their data, but keeps some data the same, we want to ignore
		#The validation cases where their email already exists
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()
			if user:
				raise ValidationError('That username is taken. Please choose a different one.')

	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()
			if user:
				raise ValidationError('An account already exists with this email.')

#Reset email reset form
class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request password reset')

	#Check the email doesn't exist, so we don't accidentally request a reset for None email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError('There is no account with that email.')

#The form used to acctual update someone's email
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Reset Password')