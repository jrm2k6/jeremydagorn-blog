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
from publishr.tests.test_database_exporter import DatabaseExporterTest
from publishr.tests.test_add_global_env_jinja import VerifyGoogleAnalyticsTest
from publishr.tests.test_template_filters import TemplateFilterPluralizeTest
from publishr.tests.test_post_exporter import PostsExporterAuthorizeUrlTest


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
        loader.loadTestsFromTestCase(DatabaseExporterTest),
        loader.loadTestsFromTestCase(SaveFileTest),
        loader.loadTestsFromTestCase(VerifyGoogleAnalyticsTest),
        loader.loadTestsFromTestCase(TemplateFilterPluralizeTest),
        loader.loadTestsFromTestCase(PostsExporterAuthorizeUrlTest)
        ))

    runner = TextTestRunner(verbosity=2)
    result = runner.run(suite)

    sys.exit(not result.wasSuccessful())
