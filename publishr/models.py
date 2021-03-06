import sqlalchemy
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash
from sqlalchemy.orm import class_mapper, ColumnProperty

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120), unique=True)
    posts = db.relationship('Post', backref='post_author', lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.set_password(password)

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [(prop.key, getattr(self, prop.key))
                for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @staticmethod
    def get_settable_columns():
        return User.__mapper__.c.keys()[1:]

    @classmethod
    def from_list(cls, fields):
        return cls(fields[0][1], fields[1][1], fields[2][1])

    @classmethod
    def has_pivot_data(cls):
        return False


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400), unique=True)
    filename = db.Column(db.String(1000))
    url = db.Column(db.String(500))
    status = db.Column(db.Integer, db.ForeignKey('status.id'))

    def __init__(self, title, filename, url, status_id):
        self.title = title
        self.filename = filename
        self.url = url
        self.status = status_id

    @classmethod
    def from_list(cls, fields):
        return cls(fields[0][1], fields[1][1], fields[2][1], fields[3][1])

    def __repr__(self):
        return '<Project %r >' % (self.title)

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [(prop.key, getattr(self, prop.key))
                for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    def row2dict(self):
        d = {}
        for prop in class_mapper(self.__class__).iterate_properties:
            if isinstance(prop, ColumnProperty):
                d[prop.key] = getattr(self, prop.key)
        return d

    @staticmethod
    def get_settable_columns():
        return Project.__mapper__.c.keys()[1:]

    @classmethod
    def has_pivot_data(cls):
        return True

    @classmethod
    def get_pivot_data(cls):
        return 'projects_technologies', 'project_id'

    @classmethod
    def get_pivot_value_col_name(cls):
        return 'projects_technologies', 'technology_id'

    @classmethod
    def get_pivot_readable_fields(cls):
        return ['Technology']


class Technology(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Technology %r>' % self.name

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [(prop.key, getattr(self, prop.key))
                for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @staticmethod
    def get_settable_columns():
        return Technology.__mapper__.c.keys()[1:]

    @classmethod
    def from_list(cls, fields):
        return cls(fields[0][1])

    @classmethod
    def has_pivot_data(cls):
        return False


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(400))
    filename_content = db.Column(db.String(1000))
    date = db.Column(db.DateTime)
    category = db.Column(db.Integer, db.ForeignKey('category.id'))
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, filename_content, date, category, author):
        self.title = title
        self.filename_content = filename_content
        self.date = date
        self.category = category
        self.author = author

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [(prop.key, getattr(self, prop.key))
                for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @staticmethod
    def get_settable_columns():
        return Post.__mapper__.c.keys()[1:]

    @classmethod
    def from_list(cls, fields):
        return cls(fields[0][1], fields[1][1], fields[2][1], fields[3][1], fields[4][1])

    @classmethod
    def has_pivot_data(cls):
        return False


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(400), unique=True)
    posts = db.relationship('Post', backref='post_category', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r  - %r >' % self.name

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [(prop.key, getattr(self, prop.key))
                for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @staticmethod
    def get_settable_columns():
        return Category.__mapper__.c.keys()[1:]

    @classmethod
    def from_list(cls, fields):
        return cls(fields[0][1])

    @classmethod
    def has_pivot_data(cls):
        return False


class Status(db.Model):
    column_list = ('id', 'status')
    editable_column = ('status')

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(400), unique=True)
    projects = db.relationship('Project', backref='project_status',
                               lazy='dynamic')

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return '<Status %r >' % self.status

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [(prop.key, getattr(self, prop.key))
                for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @staticmethod
    def get_settable_columns():
        return Status.__mapper__.c.keys()[1:]

    @classmethod
    def from_list(cls, fields):
        return cls(fields[0][1])

    @classmethod
    def has_pivot_data(cls):
        return False


class SocialNetwork(db.Model):
    column_list = ('id', 'name', 'url', 'is_shown')
    editable_column = ('name', 'url', 'is_shown')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True, nullable=False)
    url = db.Column(db.String(400), unique=True, nullable=False)
    is_shown = db.Column(db.Boolean, default=True)

    def __init__(self, name, url, is_shown):
        self.name = name
        self.url = url
        self.is_shown = is_shown

    def __repr__(self):
        return '<Social Network %r %r>' % (self.name, self.url)

    def columns(self):
        """Return the actual columns of a SQLAlchemy-mapped object"""
        return [(prop.key, getattr(self, prop.key))
                for prop in class_mapper(self.__class__).iterate_properties
                if isinstance(prop, ColumnProperty)]

    @staticmethod
    def get_settable_columns():
        return SocialNetwork.__mapper__.c.keys()[1:]

    @classmethod
    def from_list(cls, fields):
        return cls(fields[0][1])

    @classmethod
    def has_pivot_data(cls):
        return False


class ProjectsTechnologies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    technology_id = db.Column(db.Integer, db.ForeignKey('technology.id'))

    def __init__(self, project_id, technology_id):
        self.project_id = project_id
        self.technology_id = technology_id

    @classmethod
    def has_pivot_data(cls):
        return False
