from flask import Blueprint, render_template, request, flash
from flaskblog.main.forms import ContactForm
from flaskblog.models import Post

from flask_mail import Message
from flaskblog import mail

main = Blueprint('main', __name__)

#The apps are the different pages on our browse
#When passing in the route through a url_for on another page, remember to use the def name()
#Not the '/name' value
@main.route('/home')
def home():
	#User sets the page of responses
	page = request.args.get('page', 1, type=int)
	#Then we loa that page of paginations
	#Also order by most recent post
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	#We can pass variables from this app into the template
	return render_template('home.html', posts=posts)

@main.route('/')
@main.route('/landing')
@main.route('/snapto')
def snapto():
	return render_template('landing.html')

@main.route('/demo')
def demo():
	return render_template('demo.html')

@main.route('/demo2')
def demo2():
	return render_template('demo2.html')

@main.route('/donate')
def donate():
	return render_template('donate.html')

@main.route('/about')
def about():
	return render_template('about.html')

@main.route('/presskit')
def presskit():
	return render_template('presskit.html')

#The contact form works, but not in the way I want at the moment. I want to have their mail send me a mail
#But that functionality may be a little more complex. For now, It sort of is ok

@main.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()
	if form.validate_on_submit():
		msg = Message(form.email.data, sender='bonpsigames@gmail.com', recipients=['bonpsigames@gmail.com'])
		msg.body = form.content.data
		mail.send(msg)
		flash('Your message has been sent', 'success')
	return render_template('contact.html', form=form)

@main.route('/secret')
def secret():
	return render_template('errors/secret.html')