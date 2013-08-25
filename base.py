import sqlite3
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from database import init_db, connect_db, get_db, before_request, \
     close_connection

app = Flask(__name__)
app.config.from_object(__name__)


@app.route('/')
def show_entries():
    c = get_db().execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in c.fetchall()]
    return render_template('show_entries.html', entries=entries)


if __name__ == '__main__':
    app.run(debug=True)
