# -*- coding: utf-8
import os
import re
import unittest

from epub import utils
from epub.writer import epublite


def format_paragraph(paragraph):
    paragraph = paragraph.replace('--', '¡ª')
    paragraph = re.sub(r' +', ' ', paragraph)
    paragraph = re.sub(r'_(.+?)_', r'<em>\1</em>', paragraph)
    return segment_paragraph(paragraph)


def segment_paragraph(paragraph):
    segments = []
    textStart = 0
    style = []
    for match in re.finditer(r'<(/?)([^>]+)>', paragraph):
        if match.start() > textStart:
            segments.append((paragraph[textStart : match.start()], ' '.join(style)))
        if match.group(1) == '':
            style.append(match.group(2))
        else:
            style.remove(match.group(2))
        textStart = match.end()
    if textStart < len(paragraph):
        segments.append((paragraph[textStart :], ' '.join(style)))
    return segments


# XXX this code seems to be bad and doesn't actually create the text for the
# chapters; it only sets up the ToC and links for the chapters
def parse_book(filename, startLineNum, endLineNum):
    from test.writer import test_epublite as module
    PATTERN = re.compile(r'Chapter \d+$')
    sections = []
    paragraph = ''
    fin = open(os.path.join(utils.get_test_data_dir(module), filename))
    lineNum = 0
    for line in fin:
        lineNum += 1
        if lineNum < startLineNum:
            continue
        if endLineNum > 0 and lineNum > endLineNum:
            break
        line = line.strip()
        section = epublite.Section()
        if PATTERN.match(line):
            section.css = ".em { font-style: italic; }"
            section.title = line
            sections.append(section)
        elif line == '':
            if paragraph != '':
                section.text.append(format_paragraph(paragraph))
                paragraph = ''
        else:
            if paragraph != '':
                paragraph += ' '
            paragraph += line
    if paragraph != '':
        section.text.append(format_paragraph(paragraph))
    return sections


class SectionTestCase(unittest.TestCase):
    """
    """
    def test_section(self):
        pass


class BookTestCase(unittest.TestCase):
    """
    """
    def test_book(self):
        from test.writer import test_epublite as module
        book = epublite.Book(
            template_dir=utils.get_test_data_dir(module),
            display_progress=False)
        book.title = 'Pride and Prejudice'
        book.authors = ['Jane Austen']
        book.sections = parse_book('pg1342.txt', 30, 13061)
        dir = '/tmp/%s' % book.title.replace(' ', '-')
        book.make(dir, checker='../bin/epubcheck.jar')