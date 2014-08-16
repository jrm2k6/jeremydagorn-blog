import os
import unittest
import base64

from flask.ext.testing import TestCase
from flask import Flask, Markup
from . import PublisherAppTestCase
from mock import Mock
from utils import FlaskTestAuthenticationUtils, FlaskTestModelUtils, FlaskTestUtils, AssertErrorCode
from publishr.content_provider import ContentProvider, ContentNotFoundException



class FetchContentTest(PublisherAppTestCase, TestCase, AssertErrorCode, FlaskTestUtils):
    def test_load_about_not_existing(self):
        
        # given
        content_provider = ContentProvider("wrong_path")
        content_provider.load_file = Mock()
        content_provider.load_file.return_value = None
        # then
        with self.assertRaises(ContentNotFoundException):
    		content_provider.load_about()

    def test_load_about_existing(self):
        
        # given
        content_provider = ContentProvider("")
        content_provider.load_file = Mock()
        content_provider.load_file.return_value = "<p>Here is some content</p>"
        # when
        content_about = content_provider.load_about()

        # then
        self.assertEqual(str(content_about), '<p>Here is some content</p>')


if __name__ == "__main__":
    unittest.main()