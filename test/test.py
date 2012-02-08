# -*- coding: utf-8 -*-

import os
import unittest
import epub

from xml.dom import minidom

class TestFunction(unittest.TestCase):
    epub_path = '_data/test.epub'

    def test_open(self):
        test_path = os.path.join(os.path.dirname(__file__), self.epub_path)
        book = epub.open(test_path)
        
        self.assertEqual(book.opf.metadata.languages, ['en',])
        self.assertEqual(book.opf.metadata.titles, [(u'Testing Epub', ''),])
        self.assertEqual(len(book.opf.manifest.items), 7)
        for item in book.opf.manifest.items:
            self.assertIsInstance(item, epub.opf.ManifestItem)


class TestEpubFile(unittest.TestCase):
    """Test class for epub.EpubFile class"""

    epub_file = None

    def setUp(self):
        epub_file = epub.EpubFile()
        manifest = epub.opf.Manifest()
        manifest.items = [epub.opf.ManifestItem('toc', 'toc.ncx', epub.MIMETYPE_NCX),
                    epub.opf.ManifestItem('Chap001', 'Text/chap1.xhtml',
                                          epub.MIMETYPE_OPF),
                    epub.opf.ManifestItem('Chap002', 'Text/chap2.xhtml',
                                          epub.MIMETYPE_OPF),
                    ]
        epub_file.opf = epub.opf.Opf()
        epub_file.opf.manifest = manifest
        self.epub_file  = epub_file

    def test_get_item(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its id"""
        item = self.epub_file.get_item('Chap002')
        self.assertIsInstance(item, epub.opf.ManifestItem,
                              u'L\'item retourné doit être un objet de type <epub.opf.ManifestItem>')
        self.assertEqual(item.id, 'Chap002', u'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/chap2.xhtml',
                         u'href attendu incorrect.')

    def test_get_item_by_ref(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its href"""
        item = self.epub_file.get_item_by_href('Text/chap2.xhtml')
        self.assertIsInstance(item, epub.opf.ManifestItem,
                              u'L\'item retourné doit être un objet de type <epub.opf.ManifestItem>')
        self.assertEqual(item.id, 'Chap002', u'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/chap2.xhtml',
                         u'href attendu incorrect.')

