# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import unittest
import epub


from xml.dom import minidom


class TestFunction(unittest.TestCase):
    epub_path = '_data/test.epub'

    def test_get_node_text(self):
        expected_result = 'Has text.'
        xml_text = """<someNode>%s</someNode>""" % expected_result
        xml_node = minidom.parseString(xml_text).documentElement

        self.assertEquals(epub.utils.get_node_text(xml_node), expected_result)

        xml_text = """<someEmptyNode></someEmptyNode>"""
        xml_node = minidom.parseString(xml_text).documentElement

        self.assertEquals(epub.utils.get_node_text(xml_node), '')

    def test_get_urlpath_part(self):
        expected_href = 'path/to/file.html'
        expected_fragment = 'withfragment'
        url = '%s#%s' % (expected_href, expected_fragment)

        href, fragment = epub.utils.get_urlpath_part(url)
        self.assertEquals(href, expected_href)
        self.assertEquals(fragment, expected_fragment)
