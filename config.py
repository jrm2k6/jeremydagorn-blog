import os

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'jdblog.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')

UPLOAD_FOLDER = '/installation/uploads'
ALLOWED_EXTENSIONS = set(['csv'])

SECRET = 'secret'
USERNAME = 'admin'
