from unittest import TestLoader, TextTestRunner, TestSuite
from tests.test_authentication import AdminAuthenticationTest
from tests.test_render_templates import RenderTemplatesTest

if __name__ == "__main__":

    loader = TestLoader()
    suite = TestSuite((
        loader.loadTestsFromTestCase(AdminAuthenticationTest),
        loader.loadTestsFromTestCase(RenderTemplatesTest),
        ))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)