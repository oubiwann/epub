# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os


def get_node_text(node):
    """
    Return the text content of an xml.dom Element Node.

    If node does not have content, this function return an empty string.
    """
    text = ''

    node.normalize()
    if node.firstChild and node.firstChild.data:
        text = node.firstChild.data.strip()

    return text


def get_urlpath_part(urlpath):
    """
    Return a path without url fragment (something like `#frag` at the end).

    This function allow to use path from references and NCX file to read
    item from Manifest with a correct href (without losing the fragment part).

    eg.:

        url = 'text/chapter1.xhtml#part2'
        href, fragment = get_urlpath_part(url)
        print href # 'text/chapter1.xhtml'
        print fragment # '#part2'
    """
    href = urlpath
    fragment = None
    if urlpath.count('#'):
        href, fragment = urlpath.split('#')
    return (href, fragment)


def get_module_path(module):
    return os.path.dirname(module.__file__)


def get_test_data_dir(module):
    return os.path.join(get_module_path(module), "_data")