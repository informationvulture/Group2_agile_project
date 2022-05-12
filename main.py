from unicodedata import name
from flask import Flask, render_template, redirect, flash, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from src.loginform import LoginForm
from src.regform import RegisterForm
from src.userform import UserForm
from src.submissionform import submissionForm
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os
import sqlite3, json

app = Flask('app')
secret_key = "2911DEMOWEBSITESUPERSECRETKEY"

app.config['SECRET_KEY'] = "2911DEMOWEBSITESUPERSECRETKEY"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///databases/database.db'

# changed above to only one folder

db = SQLAlchemy(app)
Bootstrap(app) 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key = True)
  username = db.Column(db.String(24), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(80))
  bio = db.Column(db.String(512), default="")

class Replit(db.Model):
  replit_id = db.Column(db.Integer, primary_key = True)
  replit_name = db.Column(db.String(32))
  replit_link = db.Column(db.String(256))
  replit_description = db.Column(db.String(512), default = "")
    
db.create_all()
db.session.commit()

@app.route('/')
def home():
  return redirect(url_for('submissions'), code=200)

@app.route('/replit', methods=['GET', 'POST'])
def index():
  if current_user.is_authenticated:
    return render_template('replit_page.html', name=current_user.username, email = current_user.email, bio=current_user.bio)
  else:
    return render_template('replit_page.html')

@app.route('/submissions', methods=['GET', 'POST'])
def submissions():
  if current_user.is_authenticated:
    return render_template('user_submissions.html', name=current_user.username, email = current_user.email, bio=current_user.bio)
  
  return render_template('user_submissions.html')

@app.route('/new_submission', methods=['GET', 'POST'])
def new_submission():

  form = submissionForm()

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
  form = UserForm()
  print(current_user)
  if form.validate_on_submit():
    current_user.bio = form.bio.data
    print(f"Changed bio to: {form.bio.data}")
    db.session.commit()
    print(f"New bio: {current_user.bio}")
    return redirect(url_for('account'))
  return render_template('account.html', name=current_user.username, email = current_user.email, bio=current_user.bio, form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username = form.username.data).first()
    if user:
      if (user.password == form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('account'))
    
  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()
  
  if form.validate_on_submit():
    check = User.query.filter_by(email = form.email.data).first()
    if form.password.data != form.user_confirm_password.data:
      print("Passwords don't match.")
    elif check:
      print("Email already in use.")
    else:
      new_user = User(username=form.username.data, email=form.email.data, password=form.password.data, bio='')
      db.session.add(new_user)
      db.session.commit()
      print("Submitted New User Account!")
      return redirect('/login')
  return render_template('signup.html', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect('/login')


@app.route('/projects/<variable>')
def to_do():
  pass

@app.route("/test")
def gitpage():
  return redirect('https://github.com/informationvulture/Group2_agile_project/')


def to_json():
  """
  Return a json representation of the database.
  """
  dbfile = './databases/database.db'

  # Create a SQL connection to our SQLite database.
  con = sqlite3.connect(dbfile)

  # Creating initial cursor.
  cur = con.cursor()

  # Create variable with the list of all users (unencrypted currently).


  cur.execute("SELECT * FROM user")
  column_names = [d[0] for d in cur.description]
  user_json_format = [dict(zip(column_names, row)) for row in cur]
  
  # Ensuring the connection is closed.
  con.close()

  return user_json_format
app.run(host='0.0.0.0', port=8080)

