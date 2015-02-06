from publishr.base import force_pluralize, spacify
import unittest


class TemplateFilterPluralizeTest(unittest.TestCase):
    def test_pluralize_regular_word(self):
        self.assertEquals(force_pluralize('regular'), 'regulars')

    def test_pluralize_irregular_y_word(self):
        self.assertEquals(force_pluralize('category'), 'categories')

    def test_pluralize_irregular_s_word(self):
        self.assertEquals(force_pluralize('status'), 'statuses')


class TemplateFilterSpacifyTest(unittest.TestCase):
	def test_spacify_lowercase_str(self):
		self.assertEquals(spacify('iamlowercase'), 'iamlowercase')

	def test_spacify_camel_case_str(self):
		self.assertEquals(spacify('IAmCamelCase'), 'I Am Camel Case')

	def test_spacify_oterh_camel_case_str(self):
		self.assertEquals(spacify('iAmCamelCase'), 'i Am Camel Case')
