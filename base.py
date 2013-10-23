import sqlite3
import markdown
from flask import Flask, Response, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from models import db, User, Project, Technology, Status, Category, Post
from forms import AddUserForm, AddProjectForm, AddStatusForm, \
     AddCategoryForm, AddTechnologyForm, AddPostForm
from flask import jsonify, json, Markup
from flaskext.markdown import Markdown
from datetime import datetime
from post_loader import load_blogpost

from authentication import requires_auth

app = Flask(__name__)
Markdown(app)
app.config.from_object(__name__)
app.config.from_object('config')
app.secret_key = 'this is my secret key'

MODELS_NAMES = {'user' : User,
     'project' : Project,
     'status' : Status,
     'technology' : Technology,
     'post' : Post,
     'category' : Category
    }

def create_app(db):
    with app.app_context():
        db.init_app(app)
        db.create_all()

create_app(db)

class PostWithContent(object):
    def __init__(self, post, content):
        self.post = post
        self.content = content


@app.route('/')
def show_home():
    to_return = []
    posts = Post.query.limit(10).all()
    for p in posts:
        content = load_blogpost('posts/' + p.content)
        content = Markup(markdown.markdown(content))
        to_return.append(PostWithContent(p, content))
    return show_home_page(to_return)

def show_home_page(list_posts):
    return render_template('home.html', posts=list_posts)

@app.route('/about')
def show_about():
    return render_template('about.html')

@app.route('/projects')
def show_projects():
    return render_template('projects.html')

@app.route('/admin')
@requires_auth
def show_admin():
	return render_template('admin.html')

@app.route('/blog')
def show_blog():
    return show_home()

@app.route('/adduser', methods=['GET', 'POST'])
@requires_auth
def add_user():
    form = AddUserForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.username.data, form.email.data,
                    form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User added', 'info')
        return redirect(url_for('add_user'))
    return render_template('_add.html', form=form, rows=User.query.all(), 
        target_model="User", fields=User.__mapper__.c.keys(), action="adduser")

@app.route('/addproject', methods=['GET', 'POST'])
@requires_auth
def add_project():
    form = AddProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project = Project(form.title.data, form.description.data,
                    form.technologies.data, form.status.data)
        db.session.add(project)
        db.session.commit()
        flash('Project added', 'info')
        return redirect(url_for('add_project'))
    return render_template('_add.html', form=form, rows=Project.query.all(), 
        target_model="Project", fields=Project.__mapper__.c.keys(), action="addproject")

@app.route('/addstatus', methods=['GET', 'POST'])
@requires_auth
def add_status():
    form = AddStatusForm(request.form)
    if request.method == 'POST' and form.validate():
        status = Status(form.status.data)
        db.session.add(status)
        db.session.commit()
        flash('Status added', 'info')
        return redirect(url_for('add_status'))
    return render_template('_add.html', form=form, rows=Status.query.all(), 
        target_model="Status", fields=Status.__mapper__.c.keys(), action="addstatus")

@app.route('/addtechnology', methods=['GET', 'POST'])
@requires_auth
def add_technology():
    form = AddTechnologyForm(request.form)
    if request.method == 'POST' and form.validate():
        technology = Technology(form.name.data)
        db.session.add(technology)
        db.session.commit()
        flash('Technology added', 'info')
        return redirect(url_for('add_technology'))
    return render_template('_add.html', form=form, rows=Technology.query.all(), 
        target_model="Technology", fields=Technology.__mapper__.c.keys(), action="addtechnology")


@app.route('/addcategory', methods=['GET', 'POST'])
@requires_auth
def add_category():
    form = AddCategoryForm(request.form)
    if request.method == 'POST' and form.validate():
        category = Category(form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('Category added', 'info')
        return redirect(url_for('add_category'))
    return render_template('_add.html', form=form, rows=Category.query.all(), 
        target_model="Category", fields=Category.__mapper__.c.keys(), action="addcategory")


@app.route('/addpost', methods=['GET', 'POST'])
@requires_auth
def add_post():
    form = AddPostForm(request.form)
    if request.method == 'POST' and form.validate():
        print form.content.data
        post = Post(form.title.data, form.content.data, datetime.now(), form.category.data, form.author.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added', 'info')
        return redirect(url_for('add_post'))
    return render_template('_add.html', form=form, rows=Post.query.all(), 
        target_model="Post", fields=Post.__mapper__.c.keys(), action="addpost")


@app.route('/delete/<model_name>/<int:_id>', methods=['POST'])
@requires_auth
def delete_resource(model_name, _id):
    row_count = MODELS_NAMES[model_name].query.filter_by(id=_id).delete()

    if row_count >= 1:
        db.session.commit()
        js = json.dumps({})
        resp = Response(js, status=200, mimetype='application/json')
    else:
        resp = Response({}, status=410, mimetype='application/json')
    return resp


@app.route('/update/<model_name>/<int:_id>', methods=['POST'])
@requires_auth
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
            post.date = datetime.now()
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
