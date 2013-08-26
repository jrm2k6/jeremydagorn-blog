import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from database import init_db, connect_db, get_db, before_request, \
     close_connection

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def show_home():
    return render_template('about.html')

@app.route('/about')
def show_about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
