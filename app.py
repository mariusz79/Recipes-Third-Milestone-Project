import os
from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_pymongo import PyMongo, pymongo
from bson.objectid import ObjectId
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, Form, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, NumberRange, Email
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
#where to redirect
login_manager.login_view = 'login'
#change message category
login_manager.login_message_category = 'info'

app.config['SECRET_KEY'] = 'secret123'
app.config['MONGO_DBNAME'] = 'task_manager'
app.config['MONGO_URI'] = os.getenv('MONGO_URI1')  # 'MONGO_URI1' is saved in environmental variables, to hide password

mongo = PyMongo(app)

now = datetime.now()
users = mongo.db.users


@login_manager.user_loader
def load_user(user_id):
    users = mongo.db.users
    user_json = users.find_one({'_id': ObjectId(user_id)})
    return User(user_json)

#create a custom User class that extends UserMixin
class User(UserMixin):
    #store the json object from MongoDB inside the User class
    def __init__(self, user_json):
        self.user_json = user_json

    # Overriding get_id is required if don't have the id property
    def get_id(self):
        object_id = self.user_json.get('_id')
        return str(object_id)

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=2, max=20)])
    confirm = PasswordField('Confirm Password', validators=[
                            DataRequired(), EqualTo('password')])

    #custom function that validates username
    def validate_username(self, username):
        form = RegisterForm(request.form)
        username = form.username.data
        user = users.find_one({'username': username})
        if user:
            raise ValidationError(
                'That username is taken. Please choose a different one.')


@app.route("/register", methods=["GET", "POST"])
def register():
    #create an instance of RegisterForm
    form = RegisterForm(request.form)
     
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        date_of_registration = now.strftime("%b %d, %Y")
        users.insert_one({'username': username, 'password': password,
                          'date_of_registration': date_of_registration})
        loginuser_json = users.find_one({'username': username})
        loginuser = User(loginuser_json)
        login_user(loginuser)
        flash('You are now registered!', 'success')
        return redirect(url_for('home'))
    return render_template("register.html", form=form, title='Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        loginuser_json = users.find_one({'username': form.username.data})
        if loginuser_json and bcrypt.check_password_hash(loginuser_json['password'], form.password.data):
            # Create a custom user and pass it to login_user:
            loginuser = User(loginuser_json)
            login_user(loginuser, remember=form.remember.data)
            #redirect to a page that user wanted to enter but wasn't logged in
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You are now logged out', 'info')
    return redirect(url_for('login'))
    
@app.route('/')
def home():
    return render_template('base.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=os.environ.get('PORT'),
            debug=True)
