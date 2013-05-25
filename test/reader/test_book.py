import os
import unittest


class TestBookChapter(unittest.TestCase):

    epub_path = os.path.join(os.path.dirname(__file__), '_data/test.epub')

    def setUp(self):
        self.epub_file = epub.open_epub(self.epub_path)
        self.book = epub.Book(self.epub_file)

    def test_read(self):
        chapter = self.book.chapters[0]
        origin = self.epub_file.get_item(chapter.identifier)
        self.assertEquals(chapter.read(),
                          self.epub_file.read_item(origin))


class TestBook(unittest.TestCase):
    """
    Test the behavior of epub.Book object.

    """

    epub_path = os.path.join(os.path.dirname(__file__), '_data/test.epub')

    def setUp(self):
        self.epub_file = epub.open_epub(self.epub_path)

    def tearDown(self):
        self.epub_file.close()

    def test_chapters(self):
        book = epub.Book(self.epub_file)
        self.assertEquals(len(book.chapters), 6)

        for chapter in book.chapters:
            self.assertIsNotNone(chapter)
            self.assertIsInstance(chapter, epub.BookChapter)

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

    def test_dc_format(self):
        self.epub_file.opf.metadata.format = 'test_format'
        book = epub.Book(self.epub_file)
        self.assertEquals(book.dc_format, 'test_format')

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