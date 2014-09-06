from . import PublisherAppTestCase
from flask.ext.testing import TestCase
from mock import Mock
from utils import FlaskTestAuthenticationUtils, FlaskTestUtils, AssertErrorCode
from publishr.installation import upload_filedata, save_file, allowed_file


class SaveFileTest(PublisherAppTestCase, TestCase, FlaskTestUtils):
    def test_allowed_file_returns_false_if_extension_not_in_extensions(self):

        # given
        _filename = "myfile.csv"
        _extensions = set(["other"])

        # when
        result = allowed_file(_filename, _extensions)

        # then
        self.assertFalse(result)

    def test_allowed_file_returns_true_if_extension_not_in_extensions(self):

        # given
        _filename = "myfile.csv"
        _extensions = set(["csv", "other"])

        # when
        result = allowed_file(_filename, _extensions)

        # then
        self.assertTrue(result)

    def test_allowed_file_returns_true_if_extensions_accepts_all(self):

        # given
        _filename = "myfile.csv"
        _extensions = set("*")

        # when
        result = allowed_file(_filename, _extensions)

        # then
        self.assertTrue(result)

    def test_allowed_file_returns_true_if_extensions_accepts_all(self):

        # given
        _filename = "myfile.csv"
        _extensions = []

        # when
        result = allowed_file(_filename, _extensions)

        # then
        self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
