from wtforms import Form, BooleanField, TextField, PasswordField, validators

class AddUserForm(Form):
	username = TextField('Username', [validators.Length(min=4, max=50)])
	email = TextField('Email Address', [validators.Length(min=6, max=100)])
	password = PasswordField('New Password', [validators.Required()])

