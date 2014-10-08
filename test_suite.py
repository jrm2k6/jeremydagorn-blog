from unittest import TestLoader, TextTestRunner, TestSuite
from publishr.tests.test_authentication import AdminAuthenticationTest
from publishr.tests.test_admin_add_resources import AdminAddItemsTest
from publishr.tests.test_render_templates import RenderTemplatesTest
from publishr.tests.test_admin_delete_resources import AdminDeleteItemsTest
from publishr.tests.test_admin_update_resources import AdminUpdateItemsTest
from publishr.tests.test_fetch_posts import FetchPostsTest
from publishr.tests.test_fetch_content import FetchContentTest
from publishr.tests.test_upload_file import SaveFileTest 
from publishr.tests.test_parse_file import ParseUploadCsvTest, PopulateDatabaseTest


import sys

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(AdminAuthenticationTest),
        loader.loadTestsFromTestCase(AdminAddItemsTest),
        loader.loadTestsFromTestCase(RenderTemplatesTest),
        loader.loadTestsFromTestCase(AdminDeleteItemsTest),
        loader.loadTestsFromTestCase(AdminUpdateItemsTest),
        loader.loadTestsFromTestCase(FetchPostsTest),
        loader.loadTestsFromTestCase(FetchContentTest),
        loader.loadTestsFromTestCase(ParseUploadCsvTest),
        loader.loadTestsFromTestCase(PopulateDatabaseTest),
        loader.loadTestsFromTestCase(SaveFileTest)
        ))

    runner = TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(not result.wasSuccessful())
