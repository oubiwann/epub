import unittest

from epub.writer import book


class ToCMapNodeTestCase(unittest.testcase):
    """
    """


class EPubItemTestCase(unittest.testcase):
    """
    """


class EPubBookTestCase(unittest.testcase):
    """
    """
    def test_book():

        def getMinimalHtml(text):
            return """<!DOCTYPE html PUBLIC "-//W3C//DTD XHtml 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
                <html xmlns="http://www.w3.org/1999/xhtml">
                <head><title>%s</title></head>
                <body><p>%s</p></body>
                </html>""" % (text, text)

        book = EpubBook()
        book.set_title('Most Wanted Tips for Aspiring Young Pirates')
        book.add_creator('Monkey D Luffy')
        book.add_creator('Guybrush Threepwood')
        book.add_meta('contributor', 'Smalltalk80', role = 'bkp')
        book.add_meta('date', '2010', event = 'publication')

        book.add_title_page()
        book.add_toc_page()
        book.add_cover(r'D:\epub\blank.png')

        book.add_css(r'main.css', 'main.css')

        n1 = book.add_html('', '1.html', getMinimalHtml('Chapter 1'))
        n11 = book.add_html('', '2.html', getMinimalHtml('Section 1.1'))
        n111 = book.add_html('', '3.html', getMinimalHtml('Subsection 1.1.1'))
        n12 = book.add_html('', '4.html', getMinimalHtml('Section 1.2'))
        n2 = book.add_html('', '5.html', getMinimalHtml('Chapter 2'))

        book.add_spine_item(n1)
        book.add_spine_item(n11)
        book.add_spine_item(n111)
        book.add_spine_item(n12)
        book.add_spine_item(n2)

        # You can use both forms to add TOC map
        #t1 = book.add_toc_map_node(n1.destPath, '1')
        #t11 = book.add_toc_map_node(n11.destPath, '1.1', parent = t1)
        #t111 = book.add_toc_map_node(n111.destPath, '1.1.1', parent = t11)
        #t12 = book.add_toc_map_node(n12.destPath, '1.2', parent = t1)
        #t2 = book.add_toc_map_node(n2.destPath, '2')

        book.add_toc_map_node(n1.destPath, '1')
        book.add_toc_map_node(n11.destPath, '1.1', 2)
        book.add_toc_map_node(n111.destPath, '1.1.1', 3)
        book.add_toc_map_node(n12.destPath, '1.2', 2)
        book.add_toc_map_node(n2.destPath, '2')

        rootDir = r'd:\epub\test'
        book.create_book(rootDir)
        EpubBook.create_archive(rootDir, rootDir + '.epub')
        EpubBook.check_epub('epubcheck-1.0.5.jar', rootDir + '.epub')