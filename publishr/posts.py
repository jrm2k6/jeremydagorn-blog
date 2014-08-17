import os
import lxml.html
import re
import sys
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
    try:
        with open(file_to_load, 'r') as f:
            content = ''.join(f.readlines())
            return content
    except IOError as e:
        return None


def get_content_as_markdown(file_to_load):
    content = load_blogpost(file_to_load)
    if content is not None:
        content = Markup(markdown.markdown(content))
        return content
    else:
        return None


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

    text_without_new_lines = ''.join(content_post.splitlines())
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
