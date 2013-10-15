import sqlite3
from flask import Flask, Response, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from models import db, User, Project, Technology, Status, Category, Post
from forms import AddUserForm, AddProjectForm, AddStatusForm, \
     AddCategoryForm, AddTechnologyForm, AddPostForm
from flask import jsonify, json
from datetime import datetime

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('config')
app.secret_key = 'this is my secret key'

with app.app_context():
	db.init_app(app)
	db.create_all()

@app.route('/')
def show_home():
    return render_template('about.html')

@app.route('/about')
def show_about():
    return render_template('about.html')

@app.route('/admin')
def show_admin():
	return render_template('admin.html')

@app.route('/adduser', methods=['GET', 'POST'])
def add_user():
    form = AddUserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User added')
    return render_template('_add.html', form=form, rows=User.query.all(), 
        target_model="User", fields=User.__mapper__.c.keys(), action="adduser")

@app.route('/addproject', methods=['GET', 'POST'])
def add_project():
    form = AddProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project = Project(form.title.data, form.description.data,
                    form.technologies.data, form.status.data)
        db.session.add(project)
        db.session.commit()
        flash('Project added')
    return render_template('_add.html', form=form, rows=Project.query.all(), 
        target_model="Project", fields=Project.__mapper__.c.keys(), action="addproject")

@app.route('/addstatus', methods=['GET', 'POST'])
def add_status():
    form = AddStatusForm(request.form)
    if request.method == 'POST' and form.validate():
        status = Status(form.status.data)
        db.session.add(status)
        db.session.commit()
        flash('Status added')
    return render_template('_add.html', form=form, rows=Status.query.all(), 
        target_model="Status", fields=Status.__mapper__.c.keys(), action="addstatus")

@app.route('/addtechnology', methods=['GET', 'POST'])
def add_technology():
    form = AddTechnologyForm(request.form)
    if request.method == 'POST' and form.validate():
        technology = Technology(form.name.data)
        db.session.add(technology)
        db.session.commit()
        flash('Technology added')
    return render_template('_add.html', form=form, rows=Technology.query.all(), 
        target_model="Technology", fields=Technology.__mapper__.c.keys(), action="addtechnology")


@app.route('/addcategory', methods=['GET', 'POST'])
def add_category():
    form = AddCategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        category = Category(form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added')
    return render_template('_add.html', form=form, rows=Category.query.all(), 
        target_model="Category", fields=Category.__mapper__.c.keys(), action="addcategory")


@app.route('/addpost', methods=['GET', 'POST'])
def add_post():
    form = AddPostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(form.title.data, form.content.data, datetime.now(), form.category.data, form.author.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added')
    return render_template('_add.html', form=form, rows=Post.query.all(), 
        target_model="Post", fields=Post.__mapper__.c.keys(), action="addpost")


@app.route('/delete/<model_name>/<int:_id>', methods=['POST'])
def delete_resource(model_name, _id):
    if model_name == 'user':
        user = User.query.filter_by(id=_id).first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
        js = json.dumps({})
        resp = Response(js, status=200, mimetype='application/json')
    else:
        resp = Response({}, status=500, mimetype='application/json')
    return resp


@app.route('/update/<model_name>/<int:_id>', methods=['POST'])
def update_resource(model_name, _id):
    if model_name == 'user':
        user = User.query.filter_by(id=_id).first()
        if user is not None:
            user.email = request.json['_email']
            user.username = request.json['_username']
    elif model_name == 'status':
        status = Status.query.filter_by(id=_id).first()
        if status is not None:
            status.status = request.json['_status']
    elif model_name == 'post':
        post = Post.query.filter_by(id=_id).first()
        if post is not None:
            post.title = request.json['_title']
            post.content = request.json['_content']
            post.date = request.json['_date']
            post.category = request.json['_category']
            post.author = request.json['_author']
    elif model_name == 'technology':
        technology = Technology.query.filter_by(id=_id).first()
        if technology is not None:
            technology.name = request.json['_name']
    elif model_name == 'category':
        category = Category.query.filter_by(id=_id).first()
        if category is not None:
            category.name = request.json['_name']
    elif model_name == 'project':
        project = Project.query.filter_by(id=_id).first()
        if project is not None:
            project.title = request.json['_title']
            project.description = request.json['_description']
            project.technologies = request.json['_technologies']
            project.status = request.json['_status']
    else:
        resp = Response({}, status=500, mimetype='application/json')
    
    db.session.commit()
    js = json.dumps({})
    resp = Response(js, status=200, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
