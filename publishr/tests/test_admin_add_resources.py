import os
from flask.ext.testing import TestCase
from flask import Flask
from publishr import base
from publishr.models import db
from . import PublisherAppTestCase
from utils import FlaskTestAuthenticationUtils, FlaskTestModelUtils
import unittest
import base64


class AdminAddItemsTest(PublisherAppTestCase, TestCase, FlaskTestAuthenticationUtils, FlaskTestModelUtils):
    def test_add_user_in_database(self):
        new_user_username = "username_test"
        res = self.get_auth_required_page_with_post_data(
            url='adduser',
            data_dict=dict(username=new_user_username, email="test@email.com", password="random"),
            username="username_test",
            password="secret_test")

        self.assert_user_with_username_exists_in_database(new_user_username)

    def test_add_category_in_database(self):
        category_name = "test_category"
        res = self.get_auth_required_page_with_post_data(
            url='addcategory',
            data_dict=dict(name=category_name),
            username="username_test",
            password="secret_test")

        self.assert_category_with_name_exists_in_database(category_name)

    def test_add_technology_in_database(self):
        technology_name = "test_technology"
        res = self.get_auth_required_page_with_post_data(
            url='addtechnology',
            data_dict=dict(name=technology_name),
            username="username_test",
            password="secret_test")

        self.assert_technology_with_name_exists_in_database(technology_name)

    def test_add_status_in_database(self):
        status_name = "test_status"
        res = self.get_auth_required_page_with_post_data(
            url='addstatus',
            data_dict=dict(status=status_name),
            username="username_test",
            password="secret_test")

        self.assert_status_with_name_exists_in_database(status_name)

    def test_add_project_in_database(self):

        self.add_status_in_database(True)
        title_project = 'title_project'
        res = self.get_auth_required_page_with_post_data(
            url='addproject',
            data_dict=dict(title=title_project, description='description',
                           technologies='technology', url='www.url.com', status=1),
            username="username_test",
            password="secret_test")

        self.assert_project_with_title_exists_in_database(title_project)

    def test_add_post_in_database(self):

        self.add_category_in_database(True)
        self.add_user_in_database(True)

        title_post = 'title_post'
        res = self.get_auth_required_page_with_post_data(
            url='addpost',
            data_dict=dict(title=title_post, filename='filename',
                           category=1, author=1),
            username="username_test",
            password="secret_test")

        self.assert_post_with_title_exists_in_database(title_post)

if __name__ == "__main__":
    unittest.main()
