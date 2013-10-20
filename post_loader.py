import os
import sys
from flask import url_for, Markup
import markdown

def load_blogpost(file_to_load):
	file_to_read = os.getcwd() + '/' + file_to_load
	with open(file_to_read, 'r') as f:
		content = ''.join(f.readlines())
	return content
