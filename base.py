import sqlite3
from flask import Flask, Response, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from models import db, User, Project, Technology, Status
from forms import AddUserForm, AddProjectForm, AddStatusForm
from flask import jsonify
from flask import json

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
            db.session.commit()
        js = json.dumps({})
        resp = Response(js, status=200, mimetype='application/json')
    else:
        resp = Response({}, status=500, mimetype='application/json')
    return resp

if __name__ == '__main__':
    app.run(debug=True)
