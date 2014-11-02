from mock import Mock
from publishr import base
from publishr.base import AppInitializer
import unittest

class VerifyGoogleAnalyticsTest(unittest.TestCase):
    def setUp(self):
        self._globals = {}
        self._config = {}

    def tearDown(self):
        self._globals = {}
        self._config = {}

    def getitem_config(self, name):
        return self._config[name]

    def setitem_globals(self, name, value):
        self._globals[name] = value

    def create_globals_mock(self, app_mock):
        app_mock.jinja_env = Mock()
        app_mock.jinja_env.globals = Mock()
        app_mock.jinja_env.globals.__setitem__ = Mock(side_effect=self.setitem_globals)
       
    def create_config_mock(self, app_mock): 
        app_mock.config = Mock()
        app_mock.config.__getitem__ = Mock(side_effect=self.getitem_config)
    
    def test_jinja_env_globals_has_correct_info_when_config_correct(self):
        # given
        app = Mock()
        self.create_globals_mock(app)

        self._config['GOOGLE_ANALYTICS_KEY'] = 'key'
        self._config['GOOGLE_ANALYTICS_DOMAIN'] = 'domain'
        
        self.create_config_mock(app) 
        
        # when
        initializer = AppInitializer(app)
        initializer.set_jinja_global_variables()

        # then
        self.assertEquals(self._globals, {'has_ga_infos': True, 
                                          'ga_key': 'key', 
                                          'ga_domain': 'domain'
                                         })
    
    def test_jinja_env_globals_raises_exception_if_key_missing(self):
        # given
        app = Mock()
        self.create_globals_mock(app)

        self._config['GOOGLE_ANALYTICS_DOMAIN'] = 'domain'
        
        self.create_config_mock(app) 
        
        # when
        initializer = AppInitializer(app)
        initializer.set_jinja_global_variables()

        # then
        self.assertFalse(self._globals['has_ga_infos']) 

    
    def test_jinja_env_globals_raises_exception_if_domain_missing(self):
        # given
        app = Mock()
        self.create_globals_mock(app)

        self._config['GOOGLE_ANALYTICS_KEY'] = 'key'
        
        self.create_config_mock(app) 
        
        # when
        initializer = AppInitializer(app)
        initializer.set_jinja_global_variables()

        # then
        self.assertFalse(self._globals['has_ga_infos']) 

    def test_jinja_env_globals_raises_exception_if_no_ga_config(self):
        # given
        app = Mock()
        self.create_globals_mock(app) 
        self.create_config_mock(app) 
        
        # when
        initializer = AppInitializer(app)
        initializer.set_jinja_global_variables()

        # then
        self.assertFalse(self._globals['has_ga_infos'])

 
if __name__ == "__main__":
    unittest.main()
