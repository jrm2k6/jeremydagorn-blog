from wtforms import Form, BooleanField, TextField, PasswordField, \
			validators, SelectField
from wtfcustomwidgets import StatusField

class AddUserForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=50)])
	email = TextField('Email Address', [validators.Length(min=6, max=100)])
	password = PasswordField('New Password', [validators.Required()])


class AddProjectForm(Form):
	title = TextField('Title', [validators.Length(min=4, max=200)])
	description = TextField('Description', [validators.Length(min=6, max=400)])
	technologies = TextField('Technologies', [validators.Length(min=6, max=400)])
	status = StatusField('Status', coerce=int)


class AddStatusForm(Form):
	status = TextField('Status', [validators.Length(min=4, max=200)])
