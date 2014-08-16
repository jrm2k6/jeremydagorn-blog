import sys
import os

from flask import url_for, Markup
import markdown

class ContentProvider(object):
	def __init__(self, path_folder_content):
		self.path_folder_content = path_folder_content

	def load_about(self):
		content = self.load_file(os.getcwd() + self.path_folder_content + 'about.md')

		if content is None:
			raise ContentNotFoundException("File does not exist: " + os.getcwd() + self.path_folder_content + 'about.md')
		else:
			return Markup(markdown.markdown(content))

	def load_file(self, path_file):
		try:
			with open(path_file, 'r') as f:
				content = ''.join(f.readlines())
				return content
		except IOError as e:
			return None


class ContentNotFoundException(Exception):
    pass