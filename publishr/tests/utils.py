from publishr.models import User, Category, Technology, Status, Project, Post
from unittest import TestCase
from publishr import base
from publishr.models import db
from datetime import datetime
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

	def get_auth_required_page_with_post_json_data(self, url, data_dict, username, password):
		res = self.client.post(
				url, 
				data=data_dict,
        		headers={'Authorization': 'Basic ' + base64.b64encode(username + ":" \
        			+ password)
        		},
        		content_type='application/json')

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

	def assert_user_has_updated_values(self, _username, new_username):
		self.assertTrue(User.query.filter_by(username=_username).first() is None)
		self.assertTrue(User.query.filter_by(username=new_username).first() is not None)

	def assert_project_has_updated_values(self, _title, new_title):
		self.assertTrue(Project.query.filter_by(title=_title).first() is None)
		self.assertTrue(Project.query.filter_by(title=new_title).first() is not None)

	def assert_category_has_updated_values(self, _name, new_name):
		self.assertTrue(Category.query.filter_by(name=_name).first() is None)
		self.assertTrue(Category.query.filter_by(name=new_name).first() is not None)

	def assert_status_has_updated_values(self, _name, new_name):
		self.assertTrue(Status.query.filter_by(status=_name).first() is None)
		self.assertTrue(Status.query.filter_by(status=new_name).first() is not None)

	def assert_technology_has_updated_values(self, _name, new_name):
		self.assertTrue(Technology.query.filter_by(name=_name).first() is None)
		self.assertTrue(Technology.query.filter_by(name=new_name).first() is not None)

	def assert_post_has_updated_values(self, _title, new_title):
		self.assertTrue(Post.query.filter_by(title=_title).first() is None)
		self.assertTrue(Post.query.filter_by(title=new_title).first() is not None)

	def add_status_in_database(self, should_commit):
		status = Status("mock_status")
		db.session.add(status)
		if should_commit:
			db.session.commit()

	def add_category_in_database(self, should_commit):
		category = Category("mock_category")
		db.session.add(category)

		if should_commit:
			db.session.commit()

	def add_user_in_database(self, should_commit):
		self.add_user_in_database_with_name('mock_user', should_commit)

	def add_user_in_database_with_name(self, name, should_commit):
		user = User(name, 'mock_email', 'mock_password')
		db.session.add(user)
		if should_commit:
			db.session.commit()

	def add_project_in_database_with_title(self, _title):
		self.add_status_in_database(False)
		project = Project(_title, '','','',1)
		db.session.add(project)
		db.session.commit()

	def add_category_in_database_with_name(self, _name):
		category = Category(_name)
		db.session.add(category)
		db.session.commit()

	def add_post_in_database_with_title(self, _title):
		self.add_category_in_database(False)
		self.add_user_in_database(False)

		post = Post(_title, '', datetime.now(), 1, 1)
		db.session.add(post)
		db.session.commit()

	def add_post_in_database_with_properties(self, _title, _filename_content):
		self.add_category_in_database(False)
		self.add_user_in_database(False)

		post = Post(_title, _filename_content, datetime.now(), 1, 1)
		db.session.add(post)
		db.session.commit()

	def add_technology_in_database_with_name(self, _name):
		technology = Technology(_name)
		db.session.add(technology)
		db.session.commit()

	def add_status_in_database_with_name(self, _name):
		status = Status(_name)
		db.session.add(status)
		db.session.commit()

class FlaskTestUtils(TestCase):
	def get_page(self, url):
		res = self.client.open(url, "GET")
		return res

class AssertErrorCode(TestCase):
	def assert410(self, res):
		self.assertTrue(res._status_code == 410)

	def assert500(self, res):
		self.assertTrue(res._status_code == 500)