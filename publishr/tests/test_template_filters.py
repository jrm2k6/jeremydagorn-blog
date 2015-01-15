from publishr.base import force_pluralize
import unittest


class TemplateFilterPluralizeTest(unittest.TestCase):
    def test_pluralize_regular_word(self):
        self.assertEquals(force_pluralize('regular'), 'regulars')

    def test_pluralize_irregular_y_word(self):
        self.assertEquals(force_pluralize('category'), 'categories')

    def test_pluralize_irregular_s_word(self):
        self.assertEquals(force_pluralize('status'), 'statuses')
