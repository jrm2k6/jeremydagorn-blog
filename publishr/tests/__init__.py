import os
from flask import Flask
from flask.ext.testing import TestCase
from unittest import TestCase
from publishr import base
from publishr.models import db


class PublisherTestCase(TestCase):
    pass


class PublisherAppTestCase(PublisherTestCase):

    def create_app(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        app = base.app
        return app

    def setUp(self):
        super(PublisherAppTestCase, self).setUp()
        self.app = self.create_app()
        base.set_config(test=True)
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        super(PublisherAppTestCase, self).tearDown()
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
