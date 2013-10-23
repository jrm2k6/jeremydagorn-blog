from flask.ext.testing import TestCase
from flask import Flask
import base
import unittest


class Tests(TestCase):
    TESTING = True

    def create_app(self):
        app = base.app
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'sqlite:////temp/jdblog_test.db'
        return app

    def setUp(self):
        self.create_app()

    def tearDown(self):
    	pass

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