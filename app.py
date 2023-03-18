from flask import Flask, render_template, flash, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user 
from webforms import LoginForm, PostForm, PasswordForm, UserForm, PasswordForm, NamerForm, SearchForm
from flask_ckeditor import CKEditor
from werkzeug.utils import secure_filename
import uuid as uuid
import os

# Create A Flask Instance
app = Flask(__name__)
# Add CKEditor
ckeditor = CKEditor(app)
# Add Database
# Olda Sqlite Database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:2009ih43@localhost/our_users'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:2009ih43@localhost/our_users'
# Secret Key!
app.config['SECRET_KEY'] = "1234"
# Initialize the Database

UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
	return Users.query.get(int(user_id))

@app.context_processor
def base():
	form = SearchForm()
	return dict(form=form)

@app.route('/admin')
@login_required
def admin():
	id = current_user.id
	if id == 15:
		return render_template("admin.html")
	else:
		flash('Sorry you must be the Admin to access this page...')
		return redirect(url_for('dashboard'))

@app.route('/search', methods=["POST"])
def search():
	form = SearchForm()
	posts = Posts.query
	if form.validate_on_submit():
		post.searched = form.searched.data
		# Query the Database
		posts = posts.filter(Posts.content.like('%' + post.searched + '%'))
		posts = posts.order_by(Posts.title).all()
		return render_template("search.html",
			form=form,
			searched=post.searched,
			posts=posts)		

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(username=form.username.data).first()
		if user:
			if check_password_hash(user.password_hash, form.password.data):
				login_user(user)
				return redirect(url_for('dashboard'))
			else:
				flash("Wrong Password - Try Again!")
		else:
			flash("Hey that user doesn't exist! Try Again...")


	return render_template('login.html', form=form)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash("You have been logged out! thanks for stopping by...")
	return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	form = UserForm()
	id = current_user.id
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favourite_color = request.form['favourite_color']
		name_to_update.username = request.form['username']
		name_to_update.about_author = request.form['about_author']
		name_to_update.profile_pic = request.files['profile_pic']


		# Grab Image Name
		pic_filename = secure_filename(name_to_update.profile_pic.filename)
		# Set UUID
		pic_name = str(uuid.uuid1()) + "_" + pic_filename
		# Save That Image
		saver = request.files['profile_pic']


		# Change it to a string to save it to a Database
		name_to_update.profile_pic = pic_name
		try:
			db.session.commit()
			saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))
			flash("User Updated Successfully!")
			return render_template("dashboard.html",
				form=form,
				name_to_update=name_to_update)
		except:
			flash("Error! Looks like there was a problem")
			return render_template("dashboard.html",
				form=form,
				name_to_update=name_to_update)
	else:
		return render_template("dashboard.html",
			form=form,
			name_to_update=name_to_update,
			id=id)
	return render_template('dashboard.html')


@app.route('/posts/delete/<int:id>')
@login_required
def delete_post(id):
	post_to_delete = Posts.query.get_or_404(id)
	id = current_user.id
	if id == post_to_delete.poster.id:
		try:
			db.session.delete(post_to_delete)
			db.session.commit()

			# Return a message
			flash('Post has been deleted')
		
			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_poseted)
			return render_template("posts.html", posts=posts)
	

		except:
			# return an error message
			flash("Whops! there was a problem deleting post try again...")
	else:
		# Return a message
			flash("You Aren't Authourised To Delete That Post!")
		
			# Grab all the posts from the database
			posts = Posts.query.order_by(Posts.date_poseted)
			return render_template("posts.html", posts=posts)

@app.route('/posts')
def posts():
	# Grab all the posts from the database
	posts = Posts.query.order_by(Posts.date_poseted)
	return render_template("posts.html", posts=posts)


@app.route('/posts/<int:id>')
def post(id):
	post = Posts.query.get_or_404(id)
	return render_template('post.html', post=post)

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):
	post = Posts.query.get_or_404(id)
	form = PostForm()
	if form.validate_on_submit():
		post.title = form.title.data
		post.slug = form.slug.data
		post.content = form.content.data
		# update database
		db.session.add(post)
		db.session.commit()
		flash("Post has been updated")
		return redirect(url_for('post', id=post.id))	

	if current_user.id == post.poster_id:
		form.title.data = post.title
		form.slug.data = post.slug
		form.content.data = post.content
		return render_template('edit_post.html', form=form)
	else:
		flash("You Aren't Authourised To Edit This Post...")
		posts = Posts.query.order_by(Posts.date_poseted)
		return render_template("posts.html", posts=posts)

# Add Post Page
@app.route('/add-post', methods=['GET', 'POST'])
#@login_required
def add_post():
	form = PostForm()

	if form.validate_on_submit():
		poster = current_user.id
		post = Posts(title=form.title.data, content=form.content.data, poster_id=poster, slug=form.slug.data)
		# Clear the form
		form.title.data = ''
		form.content.data = ''
		form.slug.data = ''

		# Add post data to database
		db.session.add(post)
		db.session.commit()

		#Retrun a meaage
		flash("Blog post submitted successfully!")

	# Redirect to the webpage
	return render_template("add_post.html", form=form)

# Json thing
@app.route('/date')
def get_current_date():
	favourite_pizza = {
	"John": "Pepperoni",
	"Mary": "Cheese",
	"Tim": "Mushrooms"
	}
	return favourite_pizza
	#return {"Date": date.today()}

@app.route('/delete/<int:id>')
@login_required
def delete(id):
	if id == current_user.id:
		user_to_delete = Users.query.get_or_404(id)
		name = None
		form = UserForm()

		try:
			db.session.delete(user_to_delete)
			db.session.commit()
			flash("User Deleted Successfully!!")
			our_users = Users.query.order_by(Users.date_added)
			return render_template("add_user.html",
			form=form,
			name=name,
			our_users=our_users)
		except:
			flash("Whoops! There was a probelm deleting user, try again...")
			return render_template("add_user.html",
			form=form, name=name, our_users=our_users)
	else:
		flash("Sorry, you can't delete that user!")
		return redirect(url_for('dashboard'))

app.app_context().push()


# Update Databse Record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
	form = UserForm()
	name_to_update = Users.query.get_or_404(id)
	if request.method == "POST":
		name_to_update.name = request.form['name']
		name_to_update.email = request.form['email']
		name_to_update.favourite_color = request.form['favourite_color']
		name_to_update.username = request.form['username']
		try:
			db.session.commit()
			flash("User Updated Successfully!")
			return render_template("update.html",
				form=form,
				name_to_update=name_to_update)
		except:
			flash("Error! Looks like there was a problem")
			return render_template("update.html",
				form=form,
				name_to_update=name_to_update)
	else:
		return render_template("update.html",
			form=form,
			name_to_update=name_to_update,
			id=id)

#def index():
#	return "<h1>Hello World!</h1>"

#FILTERS
#safe
#capitalize
#lower
#upper
#title
#trim
#striptags

@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
	name = None
	form = UserForm()
	if form.validate_on_submit():
		user = Users.query.filter_by(email=form.email.data).first()
		if user is None:
			# Hash the password!!!
			hashed_pw = generate_password_hash(form.password_hash.data, "sha256") 
			user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favourite_color=form.favourite_color.data, password_hash=hashed_pw)
			db.session.add(user)
			db.session.commit()
		name = form.name.data
		form.name.data = ''
		form.username.data = ''
		form.email.data = ''
		form.favourite_color.data = ''
		form.password_hash.data = ''

		flash("User Added Successfully!")
	our_users = Users.query.order_by(Users.date_added)
	return render_template("add_user.html",
		form=form,
		name=name,
		our_users=our_users)

# Create a route decorator
@app.route('/')
def index():
	first_name = "Ihsaan"
	stuff = "This is bold text"
	
	favourite_pizza = ["Pepperoni", "Cheese", "Mushrooms", 41]
	return render_template("index.html",
	 first_name=first_name,
	 stuff=stuff,
	 favourite_pizza=favourite_pizza)

# localhost:5000/user/Ihsaan
@app.route('/user/<name>')

def user(name):
	return render_template("user.html", user_name=name)

# Create Custom Error Page

# Invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

# Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template("500.html"), 500	

# Create Password Test Page
@app.route('/test_pw', methods=['GET', 'POST'])
def test_pw():
	email = None
	password = None
	pw_to_check = None
	passed = None
	form = PasswordForm()


	# Validate Form
	if form.validate_on_submit():
		email = form.email.data
		password = form.password_hash.data
		# Clear the form
		form.email.data = ''
		form.password_hash.data = ''
		
		# Lookup User By Email Address
		pw_to_check = Users.query.filter_by(email=email).first()

		# Check Hashed Password
		passed = check_password_hash(pw_to_check.password_hash, password)

	return render_template("test_pw.html", 
		email = email, 
		password = password,
		pw_to_check = pw_to_check,
		passed=passed,
		form = form)

# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	# Validate Form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
		flash("Form Submitted Successfully!")

	return render_template("name.html", 
		name = name, 
		form = form)

# #Create a blog post model
class Posts(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(255))
	content = db.Column(db.Text)
	#author = db.Column(db.String(255))
	date_poseted = db.Column(db.DateTime, default=datetime.utcnow)
	slug = db.Column(db.String(255))
	# Foriegn Key To Link Users (refer to primakry key of the user)
	poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))

# Create Model
class Users(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), nullable=False, unique=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.String(120), nullable=False, unique=True)
	favourite_color = db.Column(db.String(120))
	about_author = db.Column(db.Text(500), nullable=True)
	date_added = db.Column(db.DateTime, default=datetime.utcnow)
	profile_pic = db.Column(db.String(500), nullable=True)

	# Do Some Password Stuff
	password_hash = db.Column(db.String(128))
	# User Can Have Many Posts
	posts = db.relationship('Posts', backref='poster')


	@property
	def password(self):
		raise AttributeError('password is not a readable attribute')

	@password.setter
	def password(self, password):
		self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return check_password_hash(self.password_hash, password)

	# Create A String
	def __repr__(self):
		return '<Name %r>' % self.name