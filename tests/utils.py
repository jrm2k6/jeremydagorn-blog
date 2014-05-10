from publishr.models import User, Category, Technology, Status, Project, Post
from unittest import TestCase
from publishr import base
from publishr.models import db
import base64

class FlaskTestAuthenticationUtils(object):
	def login_with_credentials_request(self, url, username, password):
		res = self.client.open(url, "GET", 
            headers={
                'Authorization': 'Basic ' + base64.b64encode(username + ":" \
                    + password)
            })

		return res

	def get_auth_required_page_with_post_data(self, url, data_dict, username, password):
		res = self.client.post(
				url, 
				data=data_dict,
        		headers={'Authorization': 'Basic ' + base64.b64encode(username + ":" \
        			+ password)
            })

		return res

class FlaskTestModelUtils(TestCase, object):
	def assert_user_with_username_exists_in_database(self, _username):
		self.assertTrue(User.query.filter_by(username=_username).first() is not None)

	def assert_category_with_name_exists_in_database(self, _name):
		self.assertTrue(Category.query.filter_by(name=_name).first() is not None)

	def assert_technology_with_name_exists_in_database(self, _name):
		self.assertTrue(Technology.query.filter_by(name=_name).first() is not None)

	def assert_status_with_name_exists_in_database(self, _status):
		self.assertTrue(Status.query.filter_by(status=_status).first() is not None)

	def assert_project_with_title_exists_in_database(self, _title):
		self.assertTrue(Project.query.filter_by(title=_title).first() is not None)

	def assert_post_with_title_exists_in_database(self, _title):
		self.assertTrue(Post.query.filter_by(title=_title).first() is not None)

	def assert_user_with_username_exists_in_database_is_false(self, _name):
		self.assertTrue(Project.query.filter_by(title=_name).first() is None)

	def add_status_in_database(self):
		status = Status("mock_status")
		db.session.add(status)
		db.session.commit()

	def add_category_in_database(self):
		category = Category("mock_category")
		db.session.add(category)
		db.session.commit()

	def add_user_in_database(self):
		self.add_user_in_database_with_name('mock_user')

	def add_user_in_database_with_name(self, name):
		user = User(name, 'mock_email', 'mock_password')
		db.session.add(user)
		db.session.commit()