# Copyright (c) 2012, Bin Tan
# This file is distributed under the BSD Licence. See
# python-epub-builder-license.txt for details.
from genshi.template import TemplateLoader

from epub.writer import book


class Section(object):

    def __init__(self):
        self.title = ''
        self.subsections = []
        self.css = ''
        self.text = []
        self.template_filename = 'ez-section.html'


class Book(object):

    def __init__(self, title='', authors=None, cover='', lang='en-UD',
                 sections=None, template_loader=None):
        self.impl = book.EPubBook()
        self.title = title
        self.authors = authors or []
        self.cover = cover
        self.lang = lang
        self.sections = sections or []
        self.templateLoader = template_loader or TemplateLoader('templates')

    def _add_section(self, section, id, depth):
        if depth > 0:
            loader = self.templateLoader.load(section.template_filename)
            stream = loader.generate(section=section)
            html = stream.render('xhtml', doctype = 'xhtml11', drop_xml_decl = False)
            item = self.impl.add_html('', '%s.html' % id, html)
            self.impl.add_spine_item(item)
            self.impl.add_toc_map_node(item.destPath, section.title, depth)
            id += '.'
        if len(section.subsections) > 0:
            for i, subsection in enumerate(section.subsections):
                self._add_section(subsection, id + str(i + 1), depth + 1)

    def make(self, outputDir):
        outputFile = outputDir + '.epub'

        self.impl.set_title(self.title)
        self.impl.set_lang(self.lang)
        for author in self.authors:
            self.impl.add_creator(author)
        if self.cover:
            self.impl.add_cover(self.cover)
        self.impl.add_title_page()
        self.impl.add_toc_page()
        root = Section()
        root.subsections = self.sections
        self._add_section(root, 's', 0)
        self.impl.create_book(outputDir)
        self.impl.create_archive(outputDir, outputFile)
        self.impl.check_epub('epubcheck-1.0.5.jar', outputFile)
