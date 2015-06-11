from wtforms import Form, BooleanField, TextField, TextAreaField, PasswordField, \
    validators, SelectField, DateField
from wtfcustomwidgets import StatusField, CategoryField, AuthorField, TechnologyField


class AddUserForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=50)])
    email = TextField('Email Address', [validators.Length(min=6, max=100)])
    password = PasswordField('New Password', [validators.Required()])


class AddProjectForm(Form):
    title = TextField('Title', [validators.Length(min=4, max=200)])
    description = TextField('Description', [validators.Length(min=6, max=400)])
    technologies = TechnologyField('Technologies', coerce=int)
    url = TextField('Url', [validators.Length(min=6, max=600)])
    status = StatusField('Status', coerce=int)


class AddPostForm(Form):
    title = TextField('Title', [validators.Length(min=4, max=200)])
    filename_content = TextField('Content file name')
    category = CategoryField('Category', coerce=int)
    author = AuthorField('Author', coerce=int)


class AddStatusForm(Form):
    status = TextField('Status', [validators.Length(min=4, max=200)])


class AddTechnologyForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=200)])


class AddCategoryForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=200)])


class AddSocialNetworkForm(Form):
    name = TextField('Name', [validators.Length(min=4, max=200)])
    url = TextField('Url', [validators.Length(min=4, max=400)])
