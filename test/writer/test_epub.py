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
    book.setTitle('Most Wanted Tips for Aspiring Young Pirates')
    book.addCreator('Monkey D Luffy')
    book.addCreator('Guybrush Threepwood')
    book.addMeta('contributor', 'Smalltalk80', role = 'bkp')
    book.addMeta('date', '2010', event = 'publication')

    book.addTitlePage()
    book.addTocPage()
    book.addCover(r'D:\epub\blank.png')

    book.addCss(r'main.css', 'main.css')

    n1 = book.addHtml('', '1.html', getMinimalHtml('Chapter 1'))
    n11 = book.addHtml('', '2.html', getMinimalHtml('Section 1.1'))
    n111 = book.addHtml('', '3.html', getMinimalHtml('Subsection 1.1.1'))
    n12 = book.addHtml('', '4.html', getMinimalHtml('Section 1.2'))
    n2 = book.addHtml('', '5.html', getMinimalHtml('Chapter 2'))

    book.addSpineItem(n1)
    book.addSpineItem(n11)
    book.addSpineItem(n111)
    book.addSpineItem(n12)
    book.addSpineItem(n2)

    # You can use both forms to add TOC map
    #t1 = book.addTocMapNode(n1.destPath, '1')
    #t11 = book.addTocMapNode(n11.destPath, '1.1', parent = t1)
    #t111 = book.addTocMapNode(n111.destPath, '1.1.1', parent = t11)
    #t12 = book.addTocMapNode(n12.destPath, '1.2', parent = t1)
    #t2 = book.addTocMapNode(n2.destPath, '2')

    book.addTocMapNode(n1.destPath, '1')
    book.addTocMapNode(n11.destPath, '1.1', 2)
    book.addTocMapNode(n111.destPath, '1.1.1', 3)
    book.addTocMapNode(n12.destPath, '1.2', 2)
    book.addTocMapNode(n2.destPath, '2')

    rootDir = r'd:\epub\test'
    book.createBook(rootDir)
    EpubBook.createArchive(rootDir, rootDir + '.epub')
    EpubBook.checkEpub('epubcheck-1.0.5.jar', rootDir + '.epub')