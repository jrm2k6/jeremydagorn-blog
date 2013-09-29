from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(80), unique=True)
	email = db.Column(db.String(120), unique=True)
	password = db.Column(db.String(120), unique=True)
	posts = db.relationship('Post', backref = 'post_author', lazy = 'dynamic')

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = self.set_password(password)

	def set_password(self, password):
		return generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pw_hash, password)

	def __repr__(self):
		return '<User %r>' % self.username


class Project(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(400), unique=True)
	description = db.Column(db.String(1000))
	technologies = db.Column(db.String(200))
	status = db.Column(db.Integer, db.ForeignKey('status.id'))

	def __repr__(self):
		return '<Project %r  - %r >' % self.title, self.technologies 


class Technology(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(400), unique=True)

	def __repr__(self):
		return '<Technology %r  - %r >' % self.name 


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(400), unique=True)
	content = db.Column(db.String(1000))
	date = db.Column(db.DateTime)
	category = db.Column(db.Integer, db.ForeignKey('category.id'))
	author = db.Column(db.Integer, db.ForeignKey('user.id'))


class Category(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(400), unique=True)
	posts = db.relationship('Post', backref = 'post_category', lazy = 'dynamic')

	def __repr__(self):
		return '<Category %r  - %r >' % self.name 


class Status(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	status = db.Column(db.String(400), unique=True)
	projects = db.relationship('Project', backref = 'project_status', lazy = 'dynamic')

	def __repr__(self):
		return '<Status %r  - %r >' % self.status 

