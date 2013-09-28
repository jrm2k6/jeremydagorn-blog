import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from models import db, User
from forms import AddUserForm



app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_object('config')
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
        return redirect('/admin')
    return render_template('adduser.html', form=form, users=User.query.all())

if __name__ == '__main__':
    app.run(debug=True)
