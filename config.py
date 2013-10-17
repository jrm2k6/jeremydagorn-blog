import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'jdblog.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

SECRET = 'secret'
USERNAME = 'admin'