import os
from flask.ext.testing import TestCase
from flask import Flask
from publishr import base
from publishr.models import db
from . import PublisherAppTestCase
from utils import FlaskTestAuthenticationUtils, FlaskTestModelUtils, AssertErrorCode
import unittest
import base64


class FetchPostsTest(PublisherAppTestCase, TestCase, FlaskTestAuthenticationUtils, FlaskTestModelUtils, AssertErrorCode):
    def test_fetch_post_with_existing_post_in_database(self):
        #given 
        title = 'This is my post test'
        filename_content = 'post1.txt'
        self.add_post_in_database_with_properties(title, filename_content)
        
        #when
        self.get_page('/posts/this_is_my_post_test')

        #then
        self.assert_template_used('post.html')

    def test_fetch_post_with_non_existing_post_in_database(self):
        #when
        self.get_page('/posts/this_is_my_post_test')

        #then
        self.assert_template_used('404.html')

    def test_fetch_post_with_content_file_not_existing(self):
        #given 
        title = 'This is my post test'
        filename_content = 'post_not.txt'
        self.add_post_in_database_with_properties(title, filename_content)

        #when
        self.get_page('/posts/this_is_my_post_test')

        #then
        self.assert_template_used('404.html')


if __name__ == "__main__":
    unittest.main()