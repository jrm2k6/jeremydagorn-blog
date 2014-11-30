import os
from flask.ext.testing import TestCase
from flask import Flask
from mock import Mock, patch
from publishr import base
from publishr.database_exporter import DatabaseExporter, NoDatabasePathFoundException
from . import PublisherAppTestCase
from utils import FlaskTestModelUtils
import unittest


class DatabaseExporterTest(PublisherAppTestCase, TestCase):
    def test_raises_exception_if_database_not_found(self):
        with self.assertRaises(NoDatabasePathFoundException):
            exporter = DatabaseExporter("other:///test/database")

    def test_raises_exception_if_empty_path(self):
        with self.assertRaises(NoDatabasePathFoundException):
            exporter = DatabaseExporter("")

    def test_database_path(self):
        exporter = DatabaseExporter("sqlite:///test/database/test.db")
        self.assertEquals(exporter.path_database_file, 'test/database/test.db')

    # @patch('publishr.database_exporter.os.makedirs')
    # @patch('publishr.database_exporter.os.path')
    # def test_run_with_no_exports_folder_config(self, mock_os_path, mock_makedirs):
    #    exporter = DatabaseExporter("sqlite:///test/database/test.db")
    #    mock_os_path.exists.return_value = False

        # when
    #    exporter.run()

        # then
    #    self.assertTrue(mock_makedirs.called)
