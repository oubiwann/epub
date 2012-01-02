# -*- coding: utf-8 -*-

"""
Bibliothèque de lecture des epubs
"""

__author__ = u'Florian Strzelecki <florian.strzelecki@gmail.com>'
__version__ = u'0.0.1'

import os
import zipfile

from xml.dom import minidom

CONTAINER_NAMESPACE = u'{urn:oasis:names:tc:opendocument:xmlns:container}'
MIMETYPE_OPF = u'application/oebps-package+xml'
MIMETYPE_NCX = u'application/x-dtbncx+xml'

def open(filename):
    """
    Ouvre un fichier epub et retourne un objet EpubFile représentant ce fichier.
    Le fichier est ouvert en lecture seule.
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
    book.toc = parse_toc(book.read(item_toc))
    return book

def parse_toc(xmlstring):
    """Parse un document xml NCX à partir d'une chaîne de caractères."""
    ncx = EpubNcx()
    ncx_xml = minidom.parseString(xmlstring).documentElement
    head = ncx_xml.getElementsByTagName(u'head')[0]
    # Inspect head > meta; unknow meta are ignored
    metas = {'dtb:uid': u'',
             'dtb:depth': u'',
             'dtb:totalPageCount': u'',
             'dtb:maxPageNumber': u'',
             'dtb:generator': u''}
    for meta in head.getElementsByTagName('meta'):
        metas[meta.getAttribute('name')] = meta.getAttribute('content')
    ncx.uid = metas['dtb:uid']
    ncx.depth = metas['dtb:depth']
    ncx.total_page_count = metas['dtb:totalPageCount']
    ncx.max_page_number = metas['dtb:maxPageNumber']
    ncx.generator = metas['dtb:generator']
    # Get title (docTitle tag is required)
    ncx.title = _parse_for_text_tag(ncx_xml.getElementsByTagName('docTitle')[0])
    # Get authors (docAuthor tags are optionnal)
    for author in ncx_xml.getElementsByTagName('docAuthor'):
        ncx.authors.append(_parse_for_text_tag(author))
    # Inspect navMap
    nav_map = ncx_xml.getElementsByTagName('navMap')[0]
    for e in nav_map.childNodes:
        if e.nodeType == e.ELEMENT_NODE and e.tagName == 'navPoint':
            ncx.nav_map.add_point(_parse_xml_nav_point(e))
    # Inspect pageList (if exist)
    for page_list in ncx_xml.getElementsByTagName('pageList'):
        for page_target in page_list.getElementsByTagName('pageTarget'):
            ncx.page_list.append(_parse_xml_page_target(page_target))
    return ncx

def _parse_xml_nav_point(xml_element):
    nav_point = EpubNcxNavPoint()
    nav_point.id = xml_element.getAttribute('id')
    nav_point.class_name = xml_element.getAttribute('class')
    nav_point.play_order = xml_element.getAttribute('playOrder')
    for e in xml_element.childNodes:
        if e.nodeType == e.ELEMENT_NODE:
            if e.tagName == 'navLabel':
                nav_point.label = _parse_for_text_tag(e)
            elif e.tagName == 'content':
                nav_point.src = e.getAttribute('src')
            elif e.tagName == 'navPoint':
                nav_point.nav_point.append(_parse_xml_nav_point(e))
    return nav_point

def _parse_xml_page_target(xml_element):
    page_target = EpubNcxPageTarget()
    page_target.id = xml_element.getAttribute('id')
    page_target.value = xml_element.getAttribute('value')
    page_target.type = xml_element.getAttribute('type')
    page_target.class_name = xml_element.getAttribute('class')
    page_target.play_order = xml_element.getAttribute('playOrder')
    for e in xml_element.childNodes:
        if e.nodeType == e.ELEMENT_NODE:
            if e.tagName == 'navLabel':
                page_target.label = _parse_for_text_tag(e)
            elif e.tagName == 'content':
                page_target.src = e.getAttribute('src')
    return page_target

def _parse_for_text_tag(xml_element, name=u'text'):
    text_tag = xml_element.getElementsByTagName(name)[0]
    text_tag.normalize()
    return text_tag.firstChild.data

class EpubNcx(object):
    """Représente le contenu structuré d'un fichier NCX."""

    uid = None
    depth = None
    total_page_count = None
    max_page_number = None
    generator = None 
    title = None
    authors = []
    nav_map = None
    page_list = []
    nav_lists = []

    def __init__(self):
        self.nav_map = EpubNcxNavMap()

class EpubNcxNavMap(object):
    map = []
    def add_point(self, point):
        self.map.append(point)

class EpubNcxNavPoint(object):
    id = None
    class_name = None
    play_order = None
    label = None
    src = None
    nav_point = []

class EpubNcxPageTarget(object):
    id = None
    value = None
    type = None
    class_name = None
    play_order = None
    label = None
    src = None

class EpubFile(object):
    """Représente un fichier epub, avec ses meta-données et ses fichiers"""

    zip = None
    opf_path = None
    uid = None
    uid_id = None
    metadata = None
    manifest = []
    itemref = []
    guide = []
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
        """Récupère un item du manifest par son identifiant"""
        l = [x for x in self.manifest if x.id == id]
        if l:
            return l[0]
        else:
            return None

    def get_item_by_href(self, href):
        """Récupère un item du manifest par son attribut href"""
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
        """
        Lit un fichier contenu dans l'epub.
        
        Le paramètre item peut être le chemin de ce fichier, ou un objet 
        EpubManifestItem. Le chemin du fichier doit être relatif à l'emplacement
        du fichier OPF.
        """
        path = item
        if isinstance(item, EpubManifestItem):
            path = item.href
        dirpath = os.path.dirname(self.opf_path)
        return self.zip.read(os.path.join(dirpath, path))

    def close(self):
        """
        Ferme le fichier zip (pas forcément très utile pour le moment)
        """
        self.zip.close()

class EpubMetadata(object):
    """
    Représente les méta-données d'un epub.
    """
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
        pass

    def set_from_xml(self, xml):
        """
        Renseigne les différents éléments des méta-données à partir de
        l'élément XML Dom metadata.
        """
        for node in xml.getElementsByTagName(u'dc:title'):
            node.normalize()
            self.add_title(node.firstChild.data, node.getAttribute(u'xml:lang'))
        for node in xml.getElementsByTagName(u'dc:creator'):
            node.normalize()
            self.add_creator(node.firstChild.data,
                             node.getAttribute(u'opf:role'),
                             node.getAttribute(u'opf:file-as'))
        for node in xml.getElementsByTagName(u'dc:subject'):
            node.normalize()
            self.add_subject(node.firstChild.data)
        for node in xml.getElementsByTagName(u'dc:description'):
            node.normalize()
            self.description = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:publisher'):
            node.normalize()
            self.publisher = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:contributor'):
            node.normalize()
            self.add_contributor(node.firstChild.data,
                                 node.getAttribute(u'opf:role'),
                                 node.getAttribute(u'opf:file-as'))
        for node in xml.getElementsByTagName(u'dc:date'):
            node.normalize()
            self.date = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:type'):
            node.normalize()
            self.type = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:format'):
            node.normalize()
            self.format = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:identifier'):
            node.normalize()
            self.add_identifier(node.firstChild.data,
                                node.getAttribute(u'id'),
                                node.getAttribute(u'opf:scheme'))
        for node in xml.getElementsByTagName(u'dc:source'):
            node.normalize()
            self.source = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:language'):
            node.normalize()
            self.add_language(node.firstChild.data)
        for node in xml.getElementsByTagName(u'dc:relation'):
            node.normalize()
            self.relation = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:coverage'):
            node.normalize()
            self.coverage = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:rights'):
            node.normalize()
            self.rights = node.firstChild.data
        for node in xml.getElementsByTagName(u'dc:meta'):
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

