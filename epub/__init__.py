# -*- coding: utf-8 -*-

"""
Lib to open and manipulate epub file as described in version 2.0.1.
"""

__author__ = u'Florian Strzelecki <florian.strzelecki@gmail.com>'
__version__ = u'0.0.1'

import os
import zipfile

from xml.dom import minidom

from epub import ncx

MIMETYPE_OPF = u'application/oebps-package+xml'
MIMETYPE_NCX = u'application/x-dtbncx+xml'

def open(filename):
    """Open an epub file and return an EpubFile object

    File is opened read-only.
    """
    book = EpubFile()
    book.zip = zipfile.ZipFile(filename)

    # Read container.xml to get OPF xml file path
    xmlstring = book.zip.read('META-INF/container.xml')
    container_xml = minidom.parseString(xmlstring).documentElement

    for e in container_xml.getElementsByTagName('rootfile'):
        if e.getAttribute('media-type') == MIMETYPE_OPF:
            book.opf_path = e.getAttribute('full-path')
            break

    # Read OPF xml file
    xmlstring = book.zip.read(book.opf_path)
    package = minidom.parseString(xmlstring).documentElement

    # Store each child nodes into a dict (metadata, manifest, spine, guide)
    data = {}
    for e in package.childNodes:
        if e.nodeType == e.ELEMENT_NODE:
            data[e.tagName.lower()] = e

    # Inspect metadata
    book.uid_id = package.getAttribute('unique-identifier')
    metadata = EpubMetadata()
    metadata.set_from_xml(data['metadata'])
    book.metadata = metadata

    # Get Uid
    uid = [x for x in book.metadata.identifier if x[1] == book.uid_id][0]
    book.uid = (uid[0], uid[2])

    # Inspect manifest
    for e in data['manifest'].childNodes:
        if e.nodeType == e.ELEMENT_NODE:
            book.add_item(e.getAttribute('id'), e.getAttribute('href'),
                          e.getAttribute('media-type'),
                          e.getAttribute('fallback'),
                          e.getAttribute('required-namespace'),
                          e.getAttribute('required-modules'),
                          e.getAttribute('fallback-style'))

    # Inspect spine
    item_toc = book.get_item(data['spine'].getAttribute('toc'))

    for e in data['spine'].childNodes:
        if e.nodeType == e.ELEMENT_NODE:
            book.add_spine_itemref(e.getAttribute('idref'),
                                   e.getAttribute('linear').lower() != 'no')

    # Inspect guide if exist
    if 'guide' in data:
        for e in data['guide'].childNodes:
            if e.nodeType == e.ELEMENT_NODE:
                book.add_guide_ref(e.getAttribute('href'),
                                   e.getAttribute('type'),
                                   e.getAttribute('title'))

    # Inspect NCX toc file
    book.toc = ncx.parse_toc(book.read(item_toc))

    return book


class EpubFile(object):
    """Represents an epub file as described in version 2.0.1
    
    See http://idpf.org/epub/201"""

    zip = None
    opf_path = None
    uid = None
    uid_id = None
    metadata = None
    manifest = None
    itemref = None
    guide = None
    toc = None

    def __init__(self):
        self.zip = None
        self.opf_path = None
        self.uid = None
        self.uid_id = None
        self.metadata = None
        self.manifest = []
        self.itemref = []
        self.guide = []
        toc = None

    #
    # Manifest, spine & guide
    #

    def add_item(self, id, href, media_type=None, fallback=None, 
                 required_namespace=None, required_modules=None, 
                 fallback_style=None):
        item = EpubManifestItem(id, href, media_type,
                                fallback, required_namespace, required_modules,
                                fallback_style)
        self.manifest.append(item)

    def add_spine_itemref(self, idref, linear=True):
        self.itemref.append((idref, linear))

    def get_item(self, id):
        """Get an item from manifest through its "id" attribute.
        
        Return an EpubManifestItem if found, else None."""
        l = [x for x in self.manifest if x.id == id]
        if l:
            return l[0]
        else:
            return None

    def get_item_by_href(self, href):
        """Get an item from manifest through its "href" attribute.
        
        Return an EpubManifestItem if found, else None."""
        l = [x for x in self.manifest if x.href == href]
        if l:
            return l[0]
        else:
            return None

    def add_guide_ref(self, href, type, title):
        self.guide.append((href, type, title))

    #
    # Traitement et lecture des fichiers
    #

    def read(self, item):
        """Read a file from the epub zipfile container.
        
        "item" parameter can be the relative path to the opf file or an 
        EpubManifestItem object.
        
        Html fragments are not acceptable : the path must be exactly the same 
        as indicated in the opf file.
        """
        path = item
        if isinstance(item, EpubManifestItem):
            path = item.href
        dirpath = os.path.dirname(self.opf_path)
        return self.zip.read(os.path.join(dirpath, path))

    def close(self):
        """Close the zipfile archive.
        
        Not very usefull yet, because zipfile is open in read-only."""
        self.zip.close()


class EpubMetadata(object):
    """Represent an epub's metadatas set.
    
    See http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.2"""

    title = []
    creator = []
    subject = []
    description = None
    publisher = None
    contributor = []
    date = None
    type = None
    format = None
    identifier = []
    source = None
    language = []
    relation = None
    coverage = None
    rights = None
    meta = []

    def __init__(self):
        self.title = []
        self.creator = []
        self.subject = []
        self.description = None
        self.publisher = None
        self.contributor = []
        self.date = None
        self.type = None
        self.format = None
        self.identifier = []
        self.source = None
        self.language = []
        self.relation = None
        self.coverage = None
        self.rights = None
        self.meta = []

    def set_from_xml(self, element):
        """Extract metadata from an xml.dom.Element object (ELEMENT_NODE)

        The "<metadata>" tag has a lot of metadatas about the epub this method 
        inspect and store into object attributes (like "title" or "creator").
        """

        for node in element.getElementsByTagName(u'dc:title'):
            node.normalize()
            self.add_title(node.firstChild.data, node.getAttribute(u'xml:lang'))

        for node in element.getElementsByTagName(u'dc:creator'):
            node.normalize()
            self.add_creator(node.firstChild.data,
                             node.getAttribute(u'opf:role'),
                             node.getAttribute(u'opf:file-as'))

        for node in element.getElementsByTagName(u'dc:subject'):
            node.normalize()
            self.add_subject(node.firstChild.data)

        for node in element.getElementsByTagName(u'dc:description'):
            node.normalize()
            self.description = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:publisher'):
            node.normalize()
            self.publisher = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:contributor'):
            node.normalize()
            self.add_contributor(node.firstChild.data,
                                 node.getAttribute(u'opf:role'),
                                 node.getAttribute(u'opf:file-as'))

        for node in element.getElementsByTagName(u'dc:date'):
            node.normalize()
            self.date = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:type'):
            node.normalize()
            self.type = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:format'):
            node.normalize()
            self.format = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:identifier'):
            node.normalize()
            self.add_identifier(node.firstChild.data,
                                node.getAttribute(u'id'),
                                node.getAttribute(u'opf:scheme'))

        for node in element.getElementsByTagName(u'dc:source'):
            node.normalize()
            self.source = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:language'):
            node.normalize()
            self.add_language(node.firstChild.data)

        for node in element.getElementsByTagName(u'dc:relation'):
            node.normalize()
            self.relation = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:coverage'):
            node.normalize()
            self.coverage = node.firstChild.data

        for node in element.getElementsByTagName(u'dc:rights'):
            node.normalize()
            self.rights = node.firstChild.data

        for node in element.getElementsByTagName(u'meta'):
            self.add_meta(node.getAttribute(u'name'),
                          node.getAttribute(u'content'))

    def add_title(self, title, lang=''):
        self.title.append((title, lang))

    def add_creator(self, name, role=u'aut', file_as=u''):
        self.creator.append((name, role, file_as))

    def add_subject(self, subject):
        self.subject.append(subject)

    def add_contributor(self, name, role=u'oth', file_as=u''):
        self.contributor.append((name, role, file_as))

    def set_date(self, date, event=''):
        self.date = (date, event)

    def add_identifier(self, content, id=u'', scheme=u''):
        self.identifier.append((content, id, scheme))

    def add_language(self, lang):
        self.language.append(lang)

    def add_meta(self, name, content):
        self.meta.append((name, content))

    def get_isbn(self):
        l = [id[0] for id in self.identifier if id[2].lower() == u'isbn']
        isbn = None
        if l:
            isbn = l[0]
        return isbn

class EpubManifestItem(object):
    """Represent an item from the epub's manifest."""

    id = None
    href = None
    media_type = None
    fallback = None
    required_namespace = None
    required_modules = None
    fallback_style = None

    def __init__(self, id, href, media_type=None, fallback=None, 
                 required_namespace=None, required_modules=None, 
                 fallback_style=None):
        self.id = id
        self.href = href
        self.media_type = media_type
        self.fallback = fallback
        self.required_namespace = required_namespace
        self.required_modules = required_modules
        self.fallback_style = fallback_style
