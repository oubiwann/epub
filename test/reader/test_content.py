# -*- coding: utf-8 -*-
import os
from shutil import copy, rmtree
import unittest

from epub.reader import content, opf


TEST_XHTML_MIMETYPE = 'application/xhtml+xml'


class ContentTestCase(unittest.TestCase):
    epub_path = '_data/test.epub'

    def test_open(self):
        test_path = os.path.join(os.path.dirname(__file__), self.epub_path)
        book = content.open(test_path)

        self.assertEqual(book.opf_path, 'OEBPS/content.opf')
        self.assertEqual(book.content_path, 'OEBPS')
        self.assertEqual(book.opf.metadata.languages, ['en'])
        self.assertEqual(book.opf.metadata.titles, [('Testing Epub', '')])
        self.assertEqual(len(book.opf.manifest), 7)

        for key, item in book.opf.manifest.items():
            self.assertEqual(item.identifier, key)
            self.assertIsInstance(item, opf.ManifestItem)

        with content.open(test_path) as with_book:
            self.assertEqual(with_book.opf.metadata.languages, ['en'])
            self.assertEqual(with_book.opf.metadata.titles,
                             [('Testing Epub', '')])
            self.assertEqual(len(with_book.opf.manifest), 7)
            for key, item in with_book.opf.manifest.items():
                self.assertEqual(item.identifier, key)
                self.assertIsInstance(item, opf.ManifestItem)


class ContentWriteModeTestCase(unittest.TestCase):

    epub_path = '_data/write/test.epub'
    xhtml_item_path = '_data/write/add_item.xhtml'

    def _subtest_add_item(self, book):
        """Test very basic add_item feature.

        The purpose of this subtest is to test a very few basic featureset
        that are common to both [w]rite and [a]ppend mode.
        """
        # Test if we realy are in write/append mode
        self.assertIn(book.mode, ['a', 'w'])

        filename = os.path.join(os.path.dirname(__file__),
                                self.xhtml_item_path)
        manifest_item = opf.ManifestItem(identifier='AddItem0001',
                                              href='Text/add_item.xhtml',
                                              media_type=TEST_XHTML_MIMETYPE)
        book.add_item(filename, manifest_item, True)

        with open(filename, 'r') as f:
            expected_data = f.read()
        result_data = book.read_item(manifest_item).decode('utf-8')

        self.assertIn(manifest_item, book.opf.manifest)
        self.assertEqual(result_data, expected_data)
        self.assertIn((manifest_item.identifier, True),
                      book.opf.spine.itemrefs)


class ContentWriteModeNewTestCase(ContentWriteModeTestCase):

    def setUp(self):
        self._clean_files()

    def tearDown(self):
        self._clean_files()

    def _clean_files(self):
        filename = os.path.join(os.path.dirname(__file__), self.epub_path)
        if os.path.isfile(filename):
            os.remove(filename)

    def test_open(self):
        working_copy_filename = os.path.join(os.path.dirname(__file__),
                                             self.epub_path)

        # test that the file is correctly open in [a]ppend mode.
        book = content.open(working_copy_filename, 'w')
        self.assertEqual(book.opf_path, 'OEBPS/content.opf')
        self.assertEqual(book.content_path, 'OEBPS')
        self.assertEqual(book.opf.metadata.languages, [])
        self.assertEqual(book.opf.metadata.titles, [])
        self.assertEqual(len(book.opf.manifest), 1)
        # 1 meta file: mimetype
        # 0 content file
        self.assertEqual(len(book.namelist()), 1)

        self._subtest_add_item(book)
        book.close()


class ContentWriteModeAppendTestCase(ContentWriteModeTestCase):

    epub_source = '_data/write/source.epub'
    epub_empty = '_data/write/test_empty.epub'

    def setUp(self):
        """
        Create a copy of source epub.
        """
        source_filename = os.path.join(os.path.dirname(__file__),
                                       self.epub_source)
        working_copy_filename = os.path.join(os.path.dirname(__file__),
                                             self.epub_path)
        copy(source_filename, working_copy_filename)

        self._clean_files()

    def tearDown(self):
        """
        Destroy copy of source epub.
        """
        working_copy_filename = os.path.join(os.path.dirname(__file__),
                                             self.epub_path)
        if os.path.isfile(working_copy_filename):
            os.remove(working_copy_filename)

        self._clean_files()

    def _clean_files(self):
        working_empty_filename = os.path.join(os.path.dirname(__file__),
                                             self.epub_empty)
        if os.path.isfile(working_empty_filename):
            os.remove(working_empty_filename)

    def test_open(self):
        working_copy_filename = os.path.join(os.path.dirname(__file__),
                                             self.epub_path)

        # test that the file is correctly open in [a]ppend mode.
        book = content.open(working_copy_filename, 'a')
        self.assertEqual(book.opf_path, 'OEBPS/content.opf')
        self.assertEqual(book.content_path, 'OEBPS')
        self.assertEqual(book.opf.metadata.languages, ['fr'])
        self.assertEqual(book.opf.metadata.titles, [(u'Il \xe9tait une fois...', '')])
        self.assertEqual(len(book.opf.manifest), 2)
        # 4 meta files: mimetype, container.xml, content.opf, toc.ncx,
        # 1 content file: Section0001.xhtml
        self.assertEqual(len(book.namelist()), 5)

        self._subtest_add_item(book)
        book.close()

    def test_open_new(self):
        working_copy_filename = os.path.join(os.path.dirname(__file__),
                                             self.epub_empty)

        # test that the file is correctly open in [a]ppend mode.
        book = content.open(working_copy_filename, 'a')
        self.assertEqual(book.opf_path, 'OEBPS/content.opf')
        self.assertEqual(book.content_path, 'OEBPS')
        self.assertEqual(book.opf.metadata.languages, [])
        self.assertEqual(book.opf.metadata.titles, [])
        self.assertEqual(len(book.opf.manifest), 1)
        # 1 meta file: mimetype
        # 0 content file
        self.assertEqual(len(book.namelist()), 1)

        self._subtest_add_item(book)
        book.close()


class EpubFileTestCase(unittest.TestCase):
    """Test class for epub.EpubFile class"""

    epub_path = os.path.join(os.path.dirname(__file__), '_data/test.epub')
    extracted_dir = os.path.join(os.path.dirname(__file__), '_data/tmp')

    def setUp(self):
        self.epub_file = content.open(self.epub_path)
        if not os.path.exists(self.extracted_dir):
            os.mkdir(self.extracted_dir)

    def tearDown(self):
        self.epub_file.close()
        if os.path.exists(self.extracted_dir):
            rmtree(self.extracted_dir)

    def test_extract_item_to_path(self):
        item = self.epub_file.get_item('Section0002.xhtml')

        self.epub_file.extract_item(item, to_path=self.extracted_dir)
        extracted_filename = os.path.join(self.extracted_dir,
                                          self.epub_file.content_path,
                                          item.href)
        self.assertTrue(os.path.isfile(extracted_filename))

    def test_get_item(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its id"""
        item = self.epub_file.get_item('Section0002.xhtml')
        self.assertIsInstance(item, opf.ManifestItem,
                              'L\'item retourné doit être un objet de type <epub.opf.ManifestItem>')
        self.assertEqual(item.identifier, 'Section0002.xhtml', 'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/Section0002.xhtml',
                         'href attendu incorrect.')

        self.assertEqual(self.epub_file.get_item('BadId'), None)

    def test_get_item_by_ref(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its href"""
        item = self.epub_file.get_item_by_href('Text/Section0002.xhtml')
        self.assertIsInstance(item, opf.ManifestItem,
                              'L\'item retourné doit être un objet de type <epub.opf.ManifestItem>')
        self.assertEqual(item.identifier, 'Section0002.xhtml', 'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/Section0002.xhtml',
                         'href attendu incorrect.')

        self.assertEqual(self.epub_file.get_item_by_href('BadHref'), None)

        # Change only Id, so there is 2 item with the same href attribute
        item.identifier = 'CopyOfSection0002.xhtml'
        self.epub_file.opf.manifest.append(item)

        with self.assertRaises(LookupError):
            self.epub_file.get_item_by_href(item.href)

    def test_add_item_fail(self):
        """
        When open in read-only mode, add_item must fail.
        """
        with self.assertRaises(IOError):
            filename = '_data/write/add_item.xhtml'
            manifest_item = opf.ManifestItem(identifier='AddItem0001',
                                                  href='Text/add_item.xhtml',
                                                  media_type=TEST_XHTML_MIMETYPE)
            self.epub_file.add_item(filename, manifest_item)

        self.epub_file.close()
        with self.assertRaises(RuntimeError):
            filename = '_data/write/add_item.xhtml'
            manifest_item = opf.ManifestItem(identifier='AddItem0001',
                                                  href='Text/add_item.xhtml',
                                                  media_type=TEST_XHTML_MIMETYPE)
            self.epub_file.add_item(filename, manifest_item)

