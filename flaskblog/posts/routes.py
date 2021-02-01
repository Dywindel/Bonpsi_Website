from flask import Blueprint, redirect, render_template, url_for, flash, request, abort
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post
from flaskblog.posts.forms import PostForm

posts = Blueprint('posts', __name__)

#For the main post feed
@posts.route('/post/feed')
def postfeed():
	postarchive = Post.query.all()
	page = request.args.get('page', 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
	print (posts)
	return render_template('postfeed.html', posts=posts, postarchive=postarchive)

#The address for individual posts
@posts.route('/post/<int:post_id>')
def post(post_id):
	postarchive = Post.query.all()
	#Get the post, if it doesn't exist, return 404 error
	post = Post.query.get_or_404(post_id)
	return render_template('post.html', post=post, postarchive=postarchive)

#Route for writing a new post
@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(title=form.title.data, content=form.content.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Your post has been created!', 'success')
		return redirect(url_for('main.home'))
	return render_template('create_post.html', legend='New Post', form=form)

#For updating, editing or deleting posts
#This uses the same .html as creating a new post
#It changes the legend, it populates the form with previous content
#And it updates only the specific post upon successful validation
@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
	post = Post.query.get_or_404(post_id)
	#Only the user who created this post can update it, forbidden otherwise
	if post.author != current_user:
		abort(403)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.content = form.content.data
		#We don't need to do a .add() as this data is already in the database
		db.session.commit()
		flash('Your post has been updated!', 'success')
		return redirect(url_for('posts.post', post_id=post.id))
	#Populate the form boxes before loading them
	elif request.method == 'GET':
		form.title.data = post.title
		form.content.data = post.content
	return render_template('create_post.html', legend='Update Post', form=form)

#For deleting a post
@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
	post = Post.query.get_or_404(post_id)
	if post.author != current_user:
		abort(403)
	db.session.delete(post)
	db.session.commit()
	flash('Your post has been deleted', 'success')
	return redirect(url_for('main.home'))