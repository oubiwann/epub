import os
import sys
import unittest

from epub.writer import book


class ToCMapNodeTestCase(unittest.TestCase):
    """
    """


class EPubItemTestCase(unittest.TestCase):
    """
    """


class EPubBookTestCase(unittest.TestCase):
    """
    """
    def test_book(self):

        def getMinimalHtml(text):
            return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHtml 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head><title>%s</title></head>
                <body><p>%s</p></body>
                </html>""" % (text, text)

        #import pdb;pdb.set_trace()
        from test.writer import test_book as module
        path = os.path.join(os.path.dirname(module.__file__), "_data")
        test_book = book.EPubBook(path, display_progress=False)
        test_book.set_title('Most Wanted Tips for Aspiring Young Pirates')
        test_book.add_creator('Monkey D Luffy')
        test_book.add_creator('Guybrush Threepwood')
        test_book.add_meta('contributor', 'Smalltalk80', role = 'bkp')
        test_book.add_meta('date', '2010', event = 'publication')

        test_book.add_title_page()
        test_book.add_toc_page()
        test_book.add_cover(os.path.join(path, 'cover.jpg'))

        test_book.add_css(os.path.join(path, 'main.css'), 'main.css')

        n1 = test_book.add_html('', '1.html', getMinimalHtml('Chapter 1'))
        n11 = test_book.add_html('', '2.html', getMinimalHtml('Section 1.1'))
        n111 = test_book.add_html('', '3.html', getMinimalHtml('Subsection 1.1.1'))
        n12 = test_book.add_html('', '4.html', getMinimalHtml('Section 1.2'))
        n2 = test_book.add_html('', '5.html', getMinimalHtml('Chapter 2'))

        test_book.add_spine_item(n1)
        test_book.add_spine_item(n11)
        test_book.add_spine_item(n111)
        test_book.add_spine_item(n12)
        test_book.add_spine_item(n2)

        # You can use both forms to add TOC map
        #t1 = test_book.add_toc_map_node(n1.dest_path, '1')
        #t11 = test_book.add_toc_map_node(n11.dest_path, '1.1', parent = t1)
        #t111 = test_book.add_toc_map_node(n111.dest_path, '1.1.1', parent = t11)
        #t12 = test_book.add_toc_map_node(n12.dest_path, '1.2', parent = t1)
        #t2 = test_book.add_toc_map_node(n2.dest_path, '2')

        test_book.add_toc_map_node(n1.dest_path, '1')
        test_book.add_toc_map_node(n11.dest_path, '1.1', 2)
        test_book.add_toc_map_node(n111.dest_path, '1.1.1', 3)
        test_book.add_toc_map_node(n12.dest_path, '1.2', 2)
        test_book.add_toc_map_node(n2.dest_path, '2')

        rootDir = '/tmp/test-book'
        test_book.create_book(rootDir)
        #book.EPubBook.check_epub('../bin/epubcheck.jar', rootDir + '.epub')