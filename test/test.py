# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
import unittest
import epub


from shutil import copy


TEST_XHTML_MIMETYPE = 'application/xhtml+xml'


class TestFunction(unittest.TestCase):
    epub_path = '_data/test.epub'

    def test_version(self):
        self.assertEqual(epub.__version__, '0.5.0')

    def test_open(self):
        test_path = os.path.join(os.path.dirname(__file__), self.epub_path)
        book = epub.open(test_path)

        self.assertEqual(book.opf_path, 'OEBPS/content.opf')
        self.assertEqual(book.content_path, 'OEBPS')
        self.assertEqual(book.opf.metadata.languages, ['en'])
        self.assertEqual(book.opf.metadata.titles, [('Testing Epub', '')])
        self.assertEqual(len(book.opf.manifest), 7)

        for key, item in book.opf.manifest.items():
            self.assertEqual(item.identifier, key)
            self.assertIsInstance(item, epub.opf.ManifestItem)

        with epub.open(test_path) as with_book:
            self.assertEqual(with_book.opf.metadata.languages, ['en'])
            self.assertEqual(with_book.opf.metadata.titles,
                             [('Testing Epub', '')])
            self.assertEqual(len(with_book.opf.manifest), 7)
            for key, item in with_book.opf.manifest.items():
                self.assertEqual(item.identifier, key)
                self.assertIsInstance(item, epub.opf.ManifestItem)


class TestFunctionWriteMode(unittest.TestCase):

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
        manifest_item = epub.opf.ManifestItem(identifier='AddItem0001',
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


class TestFunctionWriteModeNew(TestFunctionWriteMode):

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
        book = epub.open(working_copy_filename, 'w')
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


class TestFunctionWriteModeAppend(TestFunctionWriteMode):

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
        book = epub.open(working_copy_filename, 'a')
        self.assertEqual(book.opf_path, 'OEBPS/content.opf')
        self.assertEqual(book.content_path, 'OEBPS')
        self.assertEqual(book.opf.metadata.languages, ['fr'])
        self.assertEqual(book.opf.metadata.titles, [('Il était une fois...', '')])
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
        book = epub.open(working_copy_filename, 'a')
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


class TestEpubFile(unittest.TestCase):
    """Test class for epub.EpubFile class"""

    epub_path = '_data/test.epub'
    extracted_dir = '_data'
    extracted_name = 'OEBPS/Text/Section0002.xhtml'

    def setUp(self):
        test_path = os.path.join(os.path.dirname(__file__), self.epub_path)
        self.epub_file = epub.open(test_path)

    def tearDown(self):
        self.epub_file.close()

        extracted_filename = os.path.join(os.getcwd(),
                                          self.extracted_name)
        if os.path.isfile(extracted_filename):
            os.remove(extracted_filename)

        extracted_filename = os.path.join(os.path.dirname(__file__),
                                          self.extracted_dir,
                                          self.extracted_name)
        if os.path.isfile(extracted_filename):
            os.remove(extracted_filename)

    def test_extract_item(self):
        item = self.epub_file.get_item('Section0002.xhtml')

        self.epub_file.extract_item(item)
        extracted_filename = os.path.join(os.getcwd(),
                                          self.extracted_name)
        self.assertTrue(os.path.isfile(extracted_filename))

    def test_extract_item_to_path(self):
        item = self.epub_file.get_item('Section0002.xhtml')
        extracted_dir = os.path.join(os.path.dirname(__file__),
                                     self.extracted_dir)

        self.epub_file.extract_item(item, to_path=extracted_dir)
        extracted_filename = os.path.join(extracted_dir,
                                          self.extracted_name)
        self.assertTrue(os.path.isfile(extracted_filename))

    def test_get_item(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its id"""
        item = self.epub_file.get_item('Section0002.xhtml')
        self.assertIsInstance(item, epub.opf.ManifestItem,
                              'L\'item retourné doit être un objet de type <epub.opf.ManifestItem>')
        self.assertEqual(item.identifier, 'Section0002.xhtml', 'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/Section0002.xhtml',
                         'href attendu incorrect.')

        self.assertEqual(self.epub_file.get_item('BadId'), None)

    def test_get_item_by_ref(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its href"""
        item = self.epub_file.get_item_by_href('Text/Section0002.xhtml')
        self.assertIsInstance(item, epub.opf.ManifestItem,
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
            manifest_item = epub.opf.ManifestItem(identifier='AddItem0001',
                                                  href='Text/add_item.xhtml',
                                                  media_type=TEST_XHTML_MIMETYPE)
            self.epub_file.add_item(filename, manifest_item)

        self.epub_file.close()
        with self.assertRaises(RuntimeError):
            filename = '_data/write/add_item.xhtml'
            manifest_item = epub.opf.ManifestItem(identifier='AddItem0001',
                                                  href='Text/add_item.xhtml',
                                                  media_type=TEST_XHTML_MIMETYPE)
            self.epub_file.add_item(filename, manifest_item)


class TestBook(unittest.TestCase):

    epub_path = '_data/test.epub'

    def setUp(self):
        test_path = os.path.join(os.path.dirname(__file__), self.epub_path)
        self.epub_file = epub.open(test_path)

    def tearDown(self):
        self.epub_file.close()

    def test_chapters(self):
        book = epub.Book(self.epub_file)
        self.assertEquals(len(book.chapters), 6)

        for chapter in book.chapters:
            self.assertIsNotNone(chapter)

    def test_extra_chapters(self):
        book = epub.Book(self.epub_file)
        self.assertEquals(len(list(book.extra_chapters)), 0)

    def test_metadata_creators(self):
        name = 'Johnson Cave'
        role = 'aut'
        file_as = 'Cave, Johnson'
        self.epub_file.opf.metadata.add_creator(name, role, file_as)
        book = epub.Book(self.epub_file)
        self.assertIn((name, role, file_as), book.creators)

    def test_metadata_description(self):
        description = self.epub_file.opf.metadata.description
        book = epub.Book(self.epub_file)
        self.assertEquals(book.description, description)

    def test_metadata_isbn(self):
        isbn = '7814-54654-4354-43545'
        self.epub_file.opf.metadata.add_identifier(isbn, 'ID_ISBN', 'isbn')
        book = epub.Book(self.epub_file)
        self.assertEquals(book.isbn, isbn)

    def test_metadata_publisher(self):
        publisher = 'TEST_PUBLISHER'
        self.epub_file.opf.metadata.publisher = publisher
        book = epub.Book(self.epub_file)
        self.assertEquals(book.publisher, publisher)

    def test_metadata_contributors(self):
        name = 'Johnson Cave'
        role = 'oth'
        file_as = 'Cave, Johnson'
        self.epub_file.opf.metadata.add_contributor(name, role, file_as)
        book = epub.Book(self.epub_file)
        self.assertIn((name, role, file_as), book.contributors)

    def test_dates(self):
        date = '2032-08-04'
        event = 'publication'
        self.epub_file.opf.metadata.add_date(date, event)
        book = epub.Book(self.epub_file)
        self.assertIn((date, event), book.dates)

    def test_dc_type(self):
        self.epub_file.opf.metadata.dc_type = 'test_type'
        book = epub.Book(self.epub_file)
        self.assertEquals(book.dc_type, 'test_type')

    def test_format(self):
        self.epub_file.opf.metadata.format = 'test_format'
        book = epub.Book(self.epub_file)
        self.assertEquals(book.format, 'test_format')

    def test_identifiers(self):
        book = epub.Book(self.epub_file)
        self.assertEquals(book.identifiers,
                          [('urn:uuid:477d1a82-a70d-4ee5-a0ff-0dddc60fd2bb',
                            'BookId',
                            'UUID')])

    def test_source(self):
        self.epub_file.opf.metadata.source = 'test_source'
        book = epub.Book(self.epub_file)
        self.assertEquals(book.source, 'test_source')

    def test_languages(self):
        lang = 'test_lang'
        self.epub_file.opf.metadata.add_language(lang)
        book = epub.Book(self.epub_file)
        self.assertIn(lang, book.languages)

    def test_relation(self):
        self.epub_file.opf.metadata.relation = 'test_relation'
        book = epub.Book(self.epub_file)
        self.assertEquals(book.relation, 'test_relation')

    def test_coverage(self):
        self.epub_file.opf.metadata.coverage = 'test_coverage'
        book = epub.Book(self.epub_file)
        self.assertEquals(book.coverage, 'test_coverage')

    def test_right(self):
        self.epub_file.opf.metadata.right = 'test_right'
        book = epub.Book(self.epub_file)
        self.assertEquals(book.right, 'test_right')

    def test_metas(self):
        name = 'meta_name'
        content = 'meta_content'
        self.epub_file.opf.metadata.add_meta(name, content)
        book = epub.Book(self.epub_file)
        self.assertIn((name, content), book.metas)

    def test_subjects(self):
        title = 'New test subject'
        self.epub_file.opf.metadata.add_subject(title)
        book = epub.Book(self.epub_file)
        self.assertIn(title, book.subjects)

    def test_titles(self):
        title = 'New test title'
        lang = 'fra_alt'
        self.epub_file.opf.metadata.add_title(title, lang)
        book = epub.Book(self.epub_file)
        self.assertIn((title, lang), book.titles)
