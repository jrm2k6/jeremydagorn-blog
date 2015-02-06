import json
import sqlite3
import markdown
import os
import memcache

from flask import Flask, Response, request, session, g, redirect, url_for, \
    abort, render_template, flash
from contextlib import closing
from models import db, User, Project, Technology, Status, Category, Post, \
    SocialNetwork
from forms import AddUserForm, AddProjectForm, AddStatusForm, \
    AddCategoryForm, AddTechnologyForm, AddPostForm, AddSocialNetworkForm
from flask import jsonify, Markup
from flaskext.markdown import Markdown
from flask.ext.assets import Environment, Bundle
from datetime import datetime
from posts import PostWithMarkdownContent, load_blogpost, generate_previews, \
    get_content_as_markdown
from content_provider import ContentProvider, ContentNotFoundException
from sqlalchemy import func

from authentication import requires_auth
from installation import upload_filedata
from database_exporter import DatabaseExporter
from database_importer import DatabaseImporter
from posts_exporter import post_exporter_factory

app = Flask(__name__)
assets = Environment(app)
Markdown(app, extensions=['codehilite'])
app.config.from_object(__name__)
app.config.from_object('publishr.config')
app.secret_key = 'this is my secret key'
memc = memcache.Client([app.config['MEMCACHED_SERVER_ADDRESS']])

MODELS_NAMES = {
    'user': User,
    'project': Project,
    'status': Status,
    'technology': Technology,
    'post': Post,
    'category': Category,
    'socialnetwork': SocialNetwork
}

app.MODELS_NAMES = MODELS_NAMES


def create_app(db):
    with app.app_context():
        initializer = AppInitializer(app)
        initializer.set_jinja_global_variables()
        db.init_app(app)
        db.create_all()


class AppInitializer:
    def __init__(self, app):
        self.app = app

    def set_jinja_global_variables(self):
        try:
            self.app.jinja_env.globals['has_ga_infos'] = True
            self.app.jinja_env.globals['ga_key'] = self.app.config['GOOGLE_ANALYTICS_KEY']
            self.app.jinja_env.globals['ga_domain'] = self.app.config['GOOGLE_ANALYTICS_DOMAIN']
        except KeyError as e:
            self.app.jinja_env.globals['has_ga_infos'] = False


def set_config(test):
    if test:
        app.config.from_object('publishr.tests.config')
    else:
        app.config.from_object('publishr.config')

create_app(db)


@app.template_filter()
def force_pluralize(word):
    last_char = word[-1]
    if last_char == 'y':
        return word[:-1] + 'ies'
    elif last_char == 's':
        return word + 'es'
    else:
        return word + 's'

@app.template_filter()
def spacify(word):
    # CamelCase model name means there are composed of several words in reality
    return reduce(lambda acc, curr: acc+ " " + curr if curr.isupper() else acc + curr, word)


@app.route('/')
def show_home():
    to_return = []
    posts = Post.query.all()
    for p in posts:
        content = load_blogpost(os.getcwd() +
                                app.config["PATH_POSTS_FOLDER"] +
                                p.filename_content)
        content = Markup(markdown.markdown(content))
        to_return.append(PostWithMarkdownContent(p, content))
    previews = generate_previews(to_return)
    return show_home_page(previews)


def show_home_page(list_previews):
    return render_template('home.html', previews_posts=list_previews)


@app.route('/about')
def show_about():
    try:
        content_provider = ContentProvider(app.config["PATH_CONTENT_FOLDER"])
        about_content = content_provider.load_about()
    except ContentNotFoundException:
        about_content = "Content not found!"
        pass
    return render_template('about.html', content=about_content)


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
    return render_template('_add.html',
                           form=form,
                           rows=User.query.all(),
                           target_model="User",
                           fields=User.__mapper__.c.keys(),
                           action="adduser")


@app.route('/addproject', methods=['GET', 'POST'])
@requires_auth
def add_project():
    form = AddProjectForm(request.form)
    if request.method == 'POST' and form.validate():
        project = Project(form.title.data, form.description.data,
                          form.technologies.data, form.url.data,
                          form.status.data)
        db.session.add(project)
        db.session.commit()
        flash('Project added', 'info')
        return redirect(url_for('add_project'))
    return render_template('_add.html',
                           form=form,
                           rows=Project.query.all(),
                           target_model="Project",
                           fields=Project.__mapper__.c.keys(),
                           action="addproject")


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
    return render_template('_add.html',
                           form=form,
                           rows=Status.query.all(),
                           target_model="Status",
                           fields=Status.__mapper__.c.keys(),
                           action="addstatus")


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
    return render_template('_add.html',
                           form=form,
                           rows=Technology.query.all(),
                           target_model="Technology",
                           fields=Technology.__mapper__.c.keys(),
                           action="addtechnology")


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
    return render_template('_add.html',
                           form=form,
                           rows=Category.query.all(),
                           target_model="Category",
                           fields=Category.__mapper__.c.keys(),
                           action="addcategory")


@app.route('/addpost', methods=['GET', 'POST'])
@requires_auth
def add_post():
    form = AddPostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = Post(form.title.data, form.filename_content.data,
                    datetime.now(), form.category.data, form.author.data)
        db.session.add(post)
        db.session.commit()
        flash('Post added', 'info')
        return redirect(url_for('add_post'))
    return render_template('_add.html',
                           form=form,
                           rows=Post.query.all(),
                           target_model="Post",
                           fields=Post.__mapper__.c.keys(),
                           action="addpost")


@app.route('/addsocialnetwork', methods=['GET', 'POST'])
@requires_auth
def add_social_network():
    form = AddSocialNetworkForm(request.form)
    if request.method == 'POST' and form.validate():
        social_network = SocialNetwork(form.name.data, form.url.data, True)
        db.session.add(social_network)
        db.session.commit()
        flash('Social Network added', 'info')
        return redirect(url_for('add_social_network'))
    return render_template('_add.html',
                           form=form,
                           rows=SocialNetwork.query.all(),
                           target_model="SocialNetwork",
                           fields=SocialNetwork.__mapper__.c.keys(),
                           action="addsocialnetwork")


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
    return Response(json.dumps(response),
                    status=200,
                    mimetype='application/json')


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
            project.filename = request.json['_filename']
            project.technologies = request.json['_technologies']
            project.url = request.json['_url']
            project.status = request.json['_status']
    elif model_name == 'social_network':
        social_network = SocialNetwork.query.filter_by(id=_id).first()
        if social_network is not None:
            social_network.name = request.json['_name']
            social_network.url = request.json['_url']
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
        path = os.getcwd() + app.config["PATH_POSTS_FOLDER"]
        content_markdown = get_content_as_markdown(path +
                                                   post.filename_content)
        if content_markdown is not None:
            post_markdown = PostWithMarkdownContent(post, content_markdown)
            return render_template("post.html", post=post_markdown)
    return render_template("404.html")


@app.route('/upload_datafile', methods=['POST'])
def upload_datafile():
    if request.method == 'POST':
        _file = request.files["file"]
        if not upload_filedata(_file):
            flash("Something went wrong while uploading, \
                check that your file is really a .csv file")
    return render_template("admin.html")


@app.route('/export_database', methods=['POST'])
def export_database():
    db_exporter = DatabaseExporter(app.config['SQLALCHEMY_DATABASE_URI'])
    db_exporter.run()
    return render_template("admin.html")


@app.route('/import_database', methods=['POST'])
def import_database():
    if request.method == 'POST':
        _file = request.files["file"]
        db_importer = DatabaseImporter(app.config['SQLALCHEMY_DATABASE_URI'], _file)
        db_importer.run()
        return render_template("admin.html")
    else:
        flash("Something went wrong while importing your file")
        return render_template("admin.html")


@app.route('/authorize_posts_backup/<export_type>', methods=['GET'])
def authorize_posts_backup(export_type):
    posts_exporter_instance = post_exporter_factory(export_type)       
    memc.set('posts_exporter_instance', posts_exporter_instance)

    authorize_url = posts_exporter_instance.get_authorize_url()
    if authorize_url is not None:
        return Response(json.dumps({"aurl": authorize_url}), status=200, mimetype='application/json')
    else:
        return Response(json.dumps({}), status=500, mimetype='application/json')


@app.route('/export_archive', methods=['GET'])
def export_archive():
    posts_exporter_instance = post_exporter_factory('archive')
    memc.set('posts_exporter_instance', posts_exporter_instance)
    return posts_exporter_instance.get_response_with_available_files()


@app.route('/submit_verification_code', methods=['POST'])
def submit_verification_code():
    verification_code_submitted = request.form['verification-code']
    posts_exporter_instance = memc.get('posts_exporter_instance')
    if verification_code_submitted is not None and posts_exporter_instance is not None:
        resp = posts_exporter_instance.verify_credentials(verification_code_submitted)
        memc.set('posts_exporter_instance', posts_exporter_instance)
        return resp
    else:
        return Response(json.dumps({}), status=500, mimetype='application/json')


@app.route('/export_files', methods=['POST'])
def export_files():
    checked_files = [v for k, v in request.form.iteritems()]
    posts_exporter_instance = memc.get('posts_exporter_instance')
    if posts_exporter_instance is not None:
        resp = posts_exporter_instance.export_posts(checked_files)
        memc.delete('posts_exporter_instance')
        return resp
    else:
        return Response(json.dumps({}), status=500, mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
