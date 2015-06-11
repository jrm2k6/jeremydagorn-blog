from models import db, Status, Category, User, Technology
from wtforms import SelectField


class StatusField(SelectField):
    def __init__(self, *args, **kwargs):
        super(StatusField, self).__init__(*args, **kwargs)
        self.choices = db.session.query(Status.id, Status.status).all()


class CategoryField(SelectField):
    def __init__(self, *args, **kwargs):
        super(CategoryField, self).__init__(*args, **kwargs)
        self.choices = db.session.query(Category.id, Category.name).all()


class AuthorField(SelectField):
    def __init__(self, *args, **kwargs):
        super(AuthorField, self).__init__(*args, **kwargs)
        self.choices = db.session.query(User.id, User.username).all()


class TechnologyField(SelectField):
    def __init__(self, *args, **kwargs):
        super(TechnologyField, self).__init__(*args, **kwargs)
        self.choices = db.session.query(Technology.id, Technology.name)
