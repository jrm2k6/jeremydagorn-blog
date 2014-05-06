import os
from flask.ext.testing import TestCase
from flask import Flask
from publishr import base
from publishr.models import db
from . import PublisherAppTestCase
from utils import FlaskTestAuthenticationUtils, FlaskTestModelUtils
import unittest
import base64

class AdminAuthenticationTest(PublisherAppTestCase, TestCase, FlaskTestAuthenticationUtils):
    def test_show_admin_with_correct_credentials_returns_200(self):
        res = self.login_with_credentials_request("admin", "username_test", "secret_test")
        self.assert200(res)

    def test_show_admin_with_incorrect_username_returns_401(self):
        res = self.login_with_credentials_request("admin", "wrong_username", "secret_test")
        self.assert401(res)

    def test_show_admin_with_incorrect_password_returns_401(self):
        res = self.login_with_credentials_request("admin", "username_test", "wrong_secret")
        self.assert401(res)

class AdminAddItemsTest(PublisherAppTestCase, TestCase, FlaskTestAuthenticationUtils, FlaskTestModelUtils):
    def test_add_user_in_database(self):
        new_user_username =  "username_test"
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


if __name__ == "__main__":
    unittest.main()