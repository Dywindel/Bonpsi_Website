import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail

#Updating picture function
def save_picture(form_picture):
	#We don't want to let the user pick their own image filename
	#As this may cause a collision with another picture
	#Instead, we will give the image name a random string
	random_hex = secrets.token_hex(8)
	#Grab the image extension
	#The underscore allows us to ignore one of the returned variables we don't need
	_, f_ext = os.path.splitext(form_picture.filename)
	picture_fn = random_hex + f_ext
	#This returns us the route path where we will store the profile picture
	picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
	#Resize the image to a thumbnail using Pillow
	output_size = (125, 125)
	i = Image.open(form_picture)
	i.thumbnail(output_size)
	#Save the image to the file system
	i.save(picture_path)
	return picture_fn

#Used for sending emails
def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='bonpsigames@gmail.com',	recipients=[user.email])
	msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you do not make this request, please ignore this email.'''
	mail.send(msg)