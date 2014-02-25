import os
from flask.ext.testing import TestCase
from flask import Flask
from publishr import base
from publishr.models import db
from . import PublisherAppTestCase
import unittest


class Tests(PublisherAppTestCase, TestCase):
    
    def setUp(self):
        super(Tests, self).setUp()

    def tearDown(self):
        super(Tests, self).tearDown()

class RenderTemplatesTest(Tests):
    render_templates = False

    def test_show_about(self):
        response = self.client.get('/about')
        self.assert_template_used('about.html')

    def test_show_home(self):
        response = self.client.get('/')
        self.assert_template_used('home.html')   

    def test_show_blog(self):
        response = self.client.get('/blog')
        self.assert_template_used('home.html')

    def test_show_projects(self):
        response = self.client.get('/projects')
        self.assert_template_used('projects.html')   


if __name__ == "__main__":
    unittest.main()