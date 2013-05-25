class BookChapter(object):

    @property
    def identifier(self):
        return self._manifest_item.identifier

    def __init__(self, book, identifier, fragment=None):
        self._book = book
        self._manifest_item = self._book.epub_file.get_item(identifier)
        self._fragment = fragment

    def read(self):
        return self._book.epub_file.read_item(self._manifest_item)


class Book(object):
    """
    This class is an attempt (work in progress) to expose a simpler object
    model than EpubFile.

    """

    def __init__(self, epub_file):
        self.epub_file = epub_file

    @property
    def creators(self):
        return self.epub_file.opf.metadata.creators

    @property
    def description(self):
        return self.epub_file.opf.metadata.description

    @property
    def isbn(self):
        return self.epub_file.opf.metadata.get_isbn()

    @property
    def publisher(self):
        return self.epub_file.opf.metadata.publisher

    @property
    def contributors(self):
        return self.epub_file.opf.metadata.contributors

    @property
    def dates(self):
        return self.epub_file.opf.metadata.dates

    @property
    def dc_type(self):
        return self.epub_file.opf.metadata.dc_type

    @property
    def dc_format(self):
        return self.epub_file.opf.metadata.format

    @property
    def identifiers(self):
        return self.epub_file.opf.metadata.identifiers

    @property
    def source(self):
        return self.epub_file.opf.metadata.source

    @property
    def languages(self):
        return self.epub_file.opf.metadata.languages

    @property
    def relation(self):
        return self.epub_file.opf.metadata.relation

    @property
    def coverage(self):
        return self.epub_file.opf.metadata.coverage

    @property
    def right(self):
        return self.epub_file.opf.metadata.right

    @property
    def metas(self):
        return self.epub_file.opf.metadata.metas

    @property
    def subjects(self):
        return self.epub_file.opf.metadata.subjects

    @property
    def titles(self):
        return self.epub_file.opf.metadata.titles

    @property
    def chapters(self):
        """
        Return a list of linear chapter from spine.
        """
        return [BookChapter(self, identifier)
                for identifier, linear in self.epub_file.opf.spine.itemrefs
                if linear]

    @property
    def extra_chapters(self):
        """
        Return a list of non-linear chapter from spine.
        """
        return [BookChapter(self, identifier)
                for identifier, linear in self.epub_file.opf.spine.itemrefs
                if not linear]