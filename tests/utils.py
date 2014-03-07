from publishr.models import User
from unittest import TestCase
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