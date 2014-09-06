import os
from flask.ext.testing import TestCase
from flask import Flask
from publishr import base
from publishr.models import db
from . import PublisherAppTestCase
from utils import FlaskTestAuthenticationUtils, FlaskTestModelUtils, AssertErrorCode
from datetime import datetime
import unittest
import base64
import json


class AdminUpdateItemsTest(PublisherAppTestCase, TestCase, FlaskTestAuthenticationUtils,
                           FlaskTestModelUtils, AssertErrorCode):
    def test_update_user_in_database(self):
        username = 'my_user'
        new_username = 'my_updated_user'
        self.add_user_in_database_with_name(username, True)
        self.assert_user_with_username_exists_in_database(username)

        res = self.get_auth_required_page_with_post_json_data(
            url='/update/user/1',
            data_dict=json.dumps({'_email': 'email', '_username': new_username}),
            username="username_test",
            password="secret_test")

        self.assert_user_has_updated_values(username, new_username)

    def test_update_project_in_database(self):
        project_title = 'my_project_name'
        new_project_title = 'my_new_project_name'
        self.add_project_in_database_with_title(project_title)
        self.assert_project_with_title_exists_in_database(project_title)

        res = self.get_auth_required_page_with_post_json_data(
            url='/update/project/1',
            data_dict=json.dumps({'_title': new_project_title, '_filename': '',
                                  '_status': '1', '_technologies': '', '_url': ''}),
            username="username_test",
            password="secret_test")

        self.assert_project_has_updated_values(project_title, new_project_title)

    def test_update_category_in_database(self):
        name = 'my_category'
        new_name = 'my_new_category'
        self.add_category_in_database_with_name(name)
        self.assert_category_with_name_exists_in_database(name)

        res = self.get_auth_required_page_with_post_json_data(
            url='/update/category/1',
            data_dict=json.dumps({'_name': new_name}),
            username="username_test",
            password="secret_test")

        self.assert_category_has_updated_values(name, new_name)

    def test_update_status_in_database(self):
        name = 'my_status'
        new_name = 'my_new_status'
        self.add_status_in_database_with_name(name)
        self.assert_status_with_name_exists_in_database(name)

        res = self.get_auth_required_page_with_post_json_data(
            url='/update/status/1',
            data_dict=json.dumps({'_status': new_name}),
            username="username_test",
            password="secret_test")

        self.assert_status_has_updated_values(name, new_name)

    def test_update_technology_in_database(self):
        name = 'my_technology'
        new_name = 'my_new_technology'
        self.add_technology_in_database_with_name(name)
        self.assert_technology_with_name_exists_in_database(name)

        res = self.get_auth_required_page_with_post_json_data(
            url='/update/technology/1',
            data_dict=json.dumps({'_name': new_name}),
            username="username_test",
            password="secret_test")

        self.assert_technology_has_updated_values(name, new_name)

    def test_update_post_in_database(self):
        title = 'my_post'
        new_title = 'my_new_post'
        self.add_post_in_database_with_title(title)
        self.assert_post_with_title_exists_in_database(title)

        res = self.get_auth_required_page_with_post_json_data(
            url='/update/post/1',
            data_dict=json.dumps({'_title': new_title, '_filename_content': '',
                                  '_author': 1, '_category': 1}),
            username="username_test",
            password="secret_test")

        self.assert_post_has_updated_values(title, new_title)

    def test_update_non_existing_model(self):
        res = self.get_auth_required_page_with_post_json_data(
            url='/update/non-existing/1',
            data_dict=json.dumps({}),
            username="username_test",
            password="secret_test")

        self.assert500(res)


if __name__ == "__main__":
    unittest.main()
