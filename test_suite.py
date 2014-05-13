from unittest import TestLoader, TextTestRunner, TestSuite
from tests.test_authentication import AdminAuthenticationTest
from tests.test_admin_add_resources import AdminAddItemsTest
from tests.test_render_templates import RenderTemplatesTest
from tests.test_admin_delete_resources import AdminDeleteItemsTest
from tests.test_admin_update_resources import AdminUpdateItemsTest
from tests.test_fetch_posts import FetchPostsTest

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(AdminAuthenticationTest),
        loader.loadTestsFromTestCase(AdminAddItemsTest),
        loader.loadTestsFromTestCase(RenderTemplatesTest),
        loader.loadTestsFromTestCase(AdminDeleteItemsTest),
        loader.loadTestsFromTestCase(AdminUpdateItemsTest),
        loader.loadTestsFromTestCase(FetchPostsTest)
        ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)