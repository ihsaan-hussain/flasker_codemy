from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create A Flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "1234"

# Create a Form class
class NamerForm(FlaskForm):
	name = StringField("What's Your Name", validators=[DataRequired()])
	submit = SubmitField("Submit")

# Create a route decorator
@app.route('/')

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


# Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	# Validate Form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''

	return render_template("name.html", 
		name = name, 
		form = form)

