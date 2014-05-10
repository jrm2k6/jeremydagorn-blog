import os
from flask.ext.testing import TestCase
from flask import Flask
from publishr import base
from publishr.models import db
from . import PublisherAppTestCase
from utils import FlaskTestAuthenticationUtils, FlaskTestModelUtils
import unittest
import base64


class AdminDeleteItemsTest(PublisherAppTestCase, TestCase, FlaskTestAuthenticationUtils, FlaskTestModelUtils):
	# no need to do it for all models, the behavior is the same
    def test_delete_user_in_database_with_existing_item(self):
    	username = 'my_user'
    	self.add_user_in_database_with_name(username)
    	self.assert_user_with_username_exists_in_database(username)

        res = self.get_auth_required_page_with_post_data(
                                url='/delete/user/1', 
                                data_dict=dict(),
                                username="username_test",
                                password="secret_test")

        self.assert_user_with_username_exists_in_database_is_false(username)


if __name__ == "__main__":
    unittest.main()