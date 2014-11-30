import os
from flask.ext.testing import TestCase
from flask import Flask
from mock import Mock, patch
from publishr import base
from publishr.models import db
from publishr.installation import upload_filedata, save_file, allowed_file, \
    populate_database, CsvUserDataParser, NoItemsGeneratedFromParsingException, \
    NonExistentModelException
from . import PublisherAppTestCase
from utils import FlaskTestModelUtils
import unittest
from datetime import datetime


class ParseUploadCsvTest(PublisherAppTestCase, TestCase):
    def test_upload_filedata_returns_false_if_extension_not_correct(self):
        # given
        uploaded_file = Mock()
        uploaded_file.filename = 'filename.oops'

        # when
        success = upload_filedata(uploaded_file)

        # then
        self.assertFalse(success)

    @patch('publishr.installation.CsvUserDataParser.parse')
    @patch('publishr.installation.save_file')
    def test_upload_filedata_raises_exception_if_parsing_empty(self, mock_save_file, mock_parse):
        # given
        uploaded_file = Mock()
        uploaded_file.filename = 'filename.csv'

        mock_parse.return_value = []
        # when
        mock_save_file.return_value = True

        # then
        with self.assertRaises(NoItemsGeneratedFromParsingException):
            upload_filedata(uploaded_file)


class PopulateDatabaseTest(PublisherAppTestCase, TestCase, FlaskTestModelUtils):
    def test_populate_database_add_user(self):
        # given
        item = Mock()
        item.type = 'user'
        item.properties = ['bob', 'bob@bob.com', 'bobpw']
        items = [item]

        # when
        populate_database(items)

        # then
        self.assert_user_with_username_exists_in_database(item.properties[0])

    def test_populate_database_add_status(self):
        # given
        item = Mock()
        item.type = 'status'
        item.properties = ['status_txt']
        items = [item]

        # when
        populate_database(items)

        # then
        self.assert_status_with_name_exists_in_database(item.properties[0])

    def test_populate_database_add_category(self):
        # given
        item = Mock()
        item.type = 'category'
        item.properties = ['cat_txt']
        items = [item]

        # when
        populate_database(items)

        # then
        self.assert_category_with_name_exists_in_database(item.properties[0])

    def test_populate_database_add_technology(self):
        # given
        item = Mock()
        item.type = 'technology'
        item.properties = ['techno_txt']
        items = [item]

        # when
        populate_database(items)

        # then
        self.assert_technology_with_name_exists_in_database(item.properties[0])

    def test_populate_database_add_project(self):
        # given
        item = Mock()
        item.type = 'project'
        item.properties = ['title', 'filename', 'techno', 'url', 1]
        items = [item]

        # when
        populate_database(items)

        # then
        self.assert_project_with_title_exists_in_database(item.properties[0])

    def test_populate_database_add_post(self):
        # given
        item = Mock()
        item.type = 'post'
        item.properties = ['title', 'filename', datetime.now(), 'category', 'author']
        items = [item]

        # when
        populate_database(items)

        # then
        self.assert_post_with_title_exists_in_database(item.properties[0])

    def test_populate_database_non_existent_model(self):
        # given
        item = Mock()
        item.type = 'random'
        item.properties = ['']
        items = [item]

        # then
        with self.assertRaises(NonExistentModelException):
            populate_database(items)


if __name__ == "__main__":
    unittest.main()
