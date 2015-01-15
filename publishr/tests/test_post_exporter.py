import os
from flask.ext.testing import TestCase
from mock import Mock, patch
from flask import Flask
from publishr import base
from publishr.models import db
from io import BytesIO
from . import PublisherAppTestCase
from utils import FlaskTestAuthenticationUtils, FlaskTestUtils, AssertErrorCode
from publishr.posts_exporter import PostsExporterArchive
import unittest
import base64
import json
import zipfile


class PostsExporterAuthorizeUrlTest(PublisherAppTestCase, TestCase, AssertErrorCode,
                                    FlaskTestAuthenticationUtils, FlaskTestUtils):
    def test_authorize_posts_backup_dropbox_returns_authorize_url(self):
        res = self.get_page('/authorize_posts_backup/dropbox')
        authorize_url = json.loads(res.data)['aurl']

        self.assert200(res)
        self.assertIsNotNone(authorize_url)

    def test_authorize_posts_backup_google_drive_returns_authorize_url(self):
        res = self.get_page('/authorize_posts_backup/google-drive')
        authorize_url = json.loads(res.data)['aurl']

        self.assert200(res)
        self.assertIsNotNone(authorize_url)

    def test_returns_500_if_not_handled_type(self):
        res = self.get_page('/authorize_posts_backup/not-handled')

        with self.assertRaises(ValueError):
            authorize_url = json.loads(res.data)['aurl']

        self.assert500(res)
