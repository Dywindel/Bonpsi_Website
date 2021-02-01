from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
									 RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)

#Route for the registration page. We need to allow the user to POST and GET data
"""
@users.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RegistrationForm()
	#This check occurs just after the user types data and hits submit
	if form.validate_on_submit():
		#If account creation was successful, we should hash the password into the database
		#.decode('utf-8') turns the hash binary data into a string
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		#Here we actually create the new User. We pass in the username, email, a hashed version
		#Of the password they created 
		newuser = User(username=form.username.data, email=form.email.data,
							password=hashed_password)
		#Push the user onto the database
		db.session.add(newuser)
		db.session.commit()
		#Flash message
		flash(f'Account created successfully for {form.username.data}! You can now log in', 'success')
		return redirect(url_for('users.login'))
	else:
		return render_template('register.html', form=form)
"""

# Route for the login page
# Remove this for main upload
@users.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = LoginForm()
	if form.validate_on_submit():
		#Check user exists based on email given
		user = User.query.filter_by(email=form.email.data).first()
		#If the user exists and the passwords match, log that user in
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			#Flask has an extension for logining in a user
			login_user(user, remember=form.remember.data)
			#Get the page the user was trying to access if they had to login beforehand
			next_page = request.args.get('next')
			#Go to that next_page, if it exists, or go home
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login unsuccessful. Please check email and password.', 'danger')
	return render_template('login.html', form=form)

#Logout route
@users.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('main.home'))

#User's account route
@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = UpdateAccountForm()
	#Updating the displayed names when they are changed
	if form.validate_on_submit():
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			current_user.image_file = picture_file
		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Your account has been updated', 'success')
		return redirect(url_for('users.account'))
	#Can't remember
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('account.html', image_file=image_file, form=form)

#Loading posts by a specific user
@users.route('/user/<string:username>')
def user_posts(username):
	#User sets the page of responses
	page = request.args.get('page', 1, type=int)
	user = User.query.filter_by(username=username).first_or_404()
	#Then we load that page of paginations
	#Also order by most recent post
	posts = Post.query.filter_by(author=user)\
		.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=5)
	#We can pass variables from this app into the template
	return render_template('user_posts.html', posts=posts, user=user)

#This route is used to request a password reset
@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
	#if current_user.is_authenticated:
	#	return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('An email has been sent with instructions to reset your password', 'info')
		return redirect(url_for('users.login'))
	return render_template('reset_request.html', form=form)

#This route is used to actually reset the password
#We also need to check the supplied token
@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
	#if current_user.is_authenticated:
	#	return redirect(url_for('main.home'))
	#This is the function we wrote earlier
	user = User.verify_reset_token(token)
	if user is None:
		flash('That token is invalid or has expired', 'warning')
		return redirect(url_for('users.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated!', 'success')
		return redirect(url_for('users.login'))
	return render_template('reset_token.html', form=form)