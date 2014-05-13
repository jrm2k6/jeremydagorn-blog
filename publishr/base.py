import json
import sqlite3
import markdown
import config
from flask import Flask, Response, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from models import db, User, Project, Technology, Status, Category, Post
from forms import AddUserForm, AddProjectForm, AddStatusForm, \
     AddCategoryForm, AddTechnologyForm, AddPostForm
from flask import jsonify, Markup
from flaskext.markdown import Markdown
from datetime import datetime
from posts import PostWithMarkdownContent, load_blogpost, generate_previews, get_content_as_markdown
from sqlalchemy import func

from authentication import requires_auth

app = Flask(__name__)
Markdown(app, extensions = ['codehilite'])
app.config.from_object(__name__)
app.config.from_object('publishr.config')
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

def set_config(test):
    if test:
        app.config.from_object('tests.config')
    else:
        app.config.from_object('publishr.config')

create_app(db)


@app.route('/')
def show_home():
    to_return = []
    posts = Post.query.all()
    for p in posts:
        content = load_blogpost(config.PATH_POSTS_FOLDER + p.filename_content)
        content = Markup(markdown.markdown(content))
        to_return.append(PostWithMarkdownContent(p, content))
    previews = generate_previews(to_return)
    return show_home_page(previews)

def show_home_page(list_previews):
    return render_template('home.html', previews_posts=list_previews)

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
                    form.technologies.data, form.url.data, form.status.data)
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
        post = Post(form.title.data, form.filename_content.data, datetime.now(), form.category.data, form.author.data)
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


@app.route('/fetch/projects/', methods=['GET'])
def fetch_projects():
    projects = Project.query.all()
    response = []
    for p in projects:
        response.append(p.row2dict())
    return Response(json.dumps(response), status=200, mimetype='application/json')


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
            post.title = request.json['_title'].strip()
            post.filename_content = request.json['_filename_content'].strip()
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
            project.url = request.json['_url']
            project.status = request.json['_status']
    else:
        return Response({}, status=500, mimetype='application/json')
    
    db.session.commit()
    js = json.dumps({})
    resp = Response(js, status=200, mimetype='application/json')
    return resp


@app.route('/posts/<post_title>', methods=['GET'])
def fetch_post(post_title):
    post_title = post_title.replace("_", " ")
    post = Post.query.filter(func.lower(Post.title) == post_title).first()
    if post is not None:
        content_markdown = get_content_as_markdown(post.filename_content)
        post_markdown = PostWithMarkdownContent(post, content_markdown)
        return render_template("post.html", post=post_markdown)
    return render_template("404.html")


@app.route('/upload_datafile', methods=['POST'])
def upload_datafile():
    return render_template("admin.html")

if __name__ == '__main__':
    app.run(debug=True)
