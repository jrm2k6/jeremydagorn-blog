from flask import Flask
from flask.ext.testing import TestCase
from unittest import TestCase
from publishr import base

class PublisherTestCase(TestCase):
    pass

class PublisherAppTestCase(PublisherTestCase):

    def create_app(self):
        app = base.app
        app.config['TESTING'] = True
        app.config['SQLITE_DATABASE_URI'] = 'sqlite:////temp/jdblog_test.db'
        return app

    def setUp(self):
        super(PublisherAppTestCase, self).setUp()
        self.app = self._create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        super(PublisherAppTestCase, self).tearDown()
        db.drop_all()
        self.app_context.pop()