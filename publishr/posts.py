import os
import lxml.html
import re
import sys
import config
from flask import url_for, Markup
import markdown

class PostWithMarkdownContent(object):
    def __init__(self, post, content):
        self.post = post
        self.content = content

class PreviewPost(object):
	def __init__(self, title, preview_content):
		self.title = title
		self.content = preview_content


def load_blogpost(file_to_load):
	file_to_read = os.getcwd() + '/' + file_to_load
	with open(file_to_read, 'r') as f:
		content = ''.join(f.readlines())
	return content

def get_content_as_markdown(file_to_load):
	content = load_blogpost(config.PATH_POSTS_FOLDER + file_to_load)
	content = Markup(markdown.markdown(content))
	return content

def generate_previews(posts):
	results = []
	for post in posts:
		preview_text = get_text_elements(post.content)
		preview = PreviewPost(post.post.title, preview_text)
		results.append(preview)
	return results

def get_text_elements(content_post):
	NB_CHAR_PREVIEWS = 400
	TEXT_ELEMENT_REGEX = re.compile('<p>(.*?)</p>')
	
	text_without_new_lines =  ''.join(content_post.splitlines())
	paragraphs = re.findall(TEXT_ELEMENT_REGEX, text_without_new_lines)

	h = lxml.html.fromstring(text_without_new_lines)
	h = h.text_content().split(".")
	preview = get_preview(h)

	return preview or 'No preview available'

def get_preview(sentences):
	NB_CHAR_PREVIEWS = 400
	current_nb_chars = 0
	preview = []

	for _sentence in sentences:
		if current_nb_chars + len(_sentence) < NB_CHAR_PREVIEWS:
			preview.append(_sentence)
			current_nb_chars += len(_sentence)
		else:
			return '. '.join(preview) + "."
