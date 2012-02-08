# -*- coding: utf-8 -*-

"""
Python lib for reading OPF formated file for epub.

OPF epub : http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm
"""

import os

from xml.dom import minidom

XMLNS_DC = u'http://purl.org/dc/elements/1.1/'
XMLNS_OPF = u'http://www.idpf.org/2007/opf'

def parse_opf(xml_string):
    opf = Opf()
    package = minidom.parseString(xml_string).documentElement
    
    # Get Uid
    opf.uid_id = package.getAttribute('unique-identifier')
    
    # Store each child nodes into a dict (metadata, manifest, spine, guide)
    data = {}
    for node in [e for e in package.childNodes if e.nodeType == e.ELEMENT_NODE]:
        data[node.tagName.lower()] = node
    
    # Inspect metadata
    opf.metadata = _parse_xml_metadata(data['metadata'])
    
    # Inspect manifest
    opf.manifest = _parse_xml_manifest(data['manifest'])
    
    # Inspect spine
    opf.spine = _parse_xml_spine(data['spine'])
    
    # Inspect guide if exist
    if 'guide' in data:
        opf.guide = _parse_xml_guide(data['guide'])
    
    return opf

def _parse_xml_metadata(element):
    """Extract metadata from an xml.dom.Element object (ELEMENT_NODE)

    The "<metadata>" tag has a lot of metadatas about the epub this method 
    inspect and store into object attributes (like "title" or "creator").
    """
    metadata = Metadata()

    for node in element.getElementsByTagName(u'dc:title'):
        node.normalize()
        metadata.add_title(node.firstChild.data, node.getAttribute(u'xml:lang'))

    for node in element.getElementsByTagName(u'dc:creator'):
        node.normalize()
        metadata.add_creator(node.firstChild.data,
                         node.getAttribute(u'opf:role'),
                         node.getAttribute(u'opf:file-as'))

    for node in element.getElementsByTagName(u'dc:subject'):
        node.normalize()
        metadata.add_subject(node.firstChild.data)

    for node in element.getElementsByTagName(u'dc:description'):
        node.normalize()
        metadata.description = node.firstChild.data

    for node in element.getElementsByTagName(u'dc:publisher'):
        node.normalize()
        metadata.publisher = node.firstChild.data

    for node in element.getElementsByTagName(u'dc:contributor'):
        node.normalize()
        metadata.add_contributor(node.firstChild.data,
                             node.getAttribute(u'opf:role'),
                             node.getAttribute(u'opf:file-as'))

    for node in element.getElementsByTagName(u'dc:date'):
        node.normalize()
        metadata.add_date(node.firstChild.data,
                          node.getAttribute(u'opf:event'))

    for node in element.getElementsByTagName(u'dc:type'):
        node.normalize()
        metadata.type = node.firstChild.data

    for node in element.getElementsByTagName(u'dc:format'):
        node.normalize()
        metadata.format = node.firstChild.data

    for node in element.getElementsByTagName(u'dc:identifier'):
        node.normalize()
        metadata.add_identifier(node.firstChild.data,
                            node.getAttribute(u'id'),
                            node.getAttribute(u'opf:scheme'))

    for node in element.getElementsByTagName(u'dc:source'):
        node.normalize()
        metadata.source = node.firstChild.data

    for node in element.getElementsByTagName(u'dc:language'):
        node.normalize()
        metadata.add_language(node.firstChild.data)

    for node in element.getElementsByTagName(u'dc:relation'):
        node.normalize()
        metadata.relation = node.firstChild.data

    for node in element.getElementsByTagName(u'dc:coverage'):
        node.normalize()
        metadata.coverage = node.firstChild.data

    for node in element.getElementsByTagName(u'dc:rights'):
        node.normalize()
        metadata.rights = node.firstChild.data

    for node in element.getElementsByTagName(u'meta'):
        metadata.add_meta(node.getAttribute(u'name'),
                      node.getAttribute(u'content'))

    return metadata

def _parse_xml_manifest(element):
    """Inspect an xml.dom.Element <manifest> and return a list of 
    epub.EpubManifestItem object."""

    manifest = Manifest()
    for e in element.getElementsByTagName('item'):
        item = ManifestItem(e.getAttribute('id'),
                            e.getAttribute('href'),
                            e.getAttribute('media-type'),
                            e.getAttribute('fallback'),
                            e.getAttribute('required-namespace'),
                            e.getAttribute('required-modules'),
                            e.getAttribute('fallback-style'))
        manifest.append(item)
    return manifest

def _parse_xml_spine(element):
    """Inspect an xml.dom.Element <spine> and return epub.opf.Spine object"""

    spine = Spine()
    spine.toc = element.getAttribute('toc')
    for e in element.getElementsByTagName('itemref'):
        spine.append((e.getAttribute('idref'),
                      e.getAttribute('linear').lower() != 'no'))
    return spine

def _parse_xml_guide(element):
    """Inspect an xml.dom.Element <guide> and return a list of ref as tuple."""

    guide = Guide()
    for e in element.getElementsByTagName('ref'):
        guide.append((e.getAttribute('href'),
                      e.getAttribute('type'),
                      e.getAttribute('title')))
    return guide


class Opf(object):
    """Represent an OPF formated file.
    
    OPF is an xml formated file, used in the epub spec."""
    
    def __init__(self):
        self.uid_id = None
        self.version = u'2.0'
        self.xmlns = XMLNS_OPF
        self.metadata = Metadata()
        self.manifest = Manifest()
        self.spine = Spine()
        self.guide = Guide()


class Metadata(object):
    """Represent an epub's metadatas set.
    
    See http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.2"""

    def __init__(self):
        self.titles = []
        self.creators = []
        self.subjects = []
        self.description = None
        self.publisher = None
        self.contributors = []
        self.dates = []
        self.type = None
        self.format = None
        self.identifiers = []
        self.source = None
        self.languages = []
        self.relation = None
        self.coverage = None
        self.right = None
        self.metas = []

    def add_title(self, title, lang=''):
        self.titles.append((title, lang))

    def add_creator(self, name, role=u'aut', file_as=u''):
        self.creators.append((name, role, file_as))

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_contributor(self, name, role=u'oth', file_as=u''):
        self.contributors.append((name, role, file_as))

    def add_date(self, date, event=''):
        self.dates.append((date, event))

    def add_identifier(self, content, id=u'', scheme=u''):
        self.identifiers.append((content, id, scheme))

    def add_language(self, lang):
        self.languages.append(lang)

    def add_meta(self, name, content):
        self.metas.append((name, content))

    def get_isbn(self):
        l = [id[0] for id in self.identifiers if id[2].lower() == u'isbn']
        isbn = None
        if l:
            isbn = l[0]
        return isbn

    def as_xml_element(self):
        """Return an xml dom Element node."""
        doc = minidom.Document()
        metadata = doc.createElement('metadata')

        for text, lang in self.titles:
            title = doc.createElement('dc:title')
            if lang:
                title.setAttribute('xml:lang', lang)
            title.appendChild(doc.createTextNode(text))
            metadata.appendChild(title)

        for name, role, file_as in self.creators:
            creator = doc.createElement('dc:creator')
            creator.setAttribute('opf:role', role)
            if file_as:
                creator.setAttribute('opf:file-as', file_as)
            creator.appendChild(doc.createTextNode(name))
            metadata.appendChild(creator)

        for text in self.subjects:
            subject = doc.createElement('dc:subject')
            subject.appendChild(doc.createTextNode(text))
            metadata.appendChild(subject)

        if self.description:
            description = doc.createElement('dc:description')
            description.appendChild(doc.createTextNode(self.description))
            metadata.appendChild(description)

        if self.publisher:
            publisher = doc.createElement('dc:publisher')
            publisher.appendChild(doc.createTextNode(self.publisher))
            metadata.appendChild(publisher)

        for name, role, file_as in self.contributors:
            contributor = doc.createElement('dc:creator')
            contributor.setAttribute('opf:role', role)
            if file_as:
                contributor.setAttribute('opf:file-as', file_as)
            contributor.appendChild(doc.createTextNode(name))
            metadata.appendChild(contributor)

        for text, event in self.dates:
            date = doc.createElement('dc:date')
            if event:
                date.setAttribute('opf:event', event)
            date.appendChild(doc.createTextNode(text))
            metadata.appendChild(date)

        if self.type:
            type = doc.createElement('dc:type')
            type.appendChild(doc.createTextNode(self.type))
            metadata.appendChild(type)

        if self.format:
            format = doc.createElement('dc:format')
            format.appendChild(doc.createTextNode(self.format))
            metadata.appendChild(format)

        for text, id, scheme in self.identifiers:
            identifier = doc.createElement('dc:identifier')
            if id:
                identifier.setAttribute('id', id)
            if scheme:
                identifier.setAttribute('opf:scheme', scheme)
            identifier.appendChild(doc.createTextNode(text))
            metadata.appendChild(identifier)

        if self.source:
            source = doc.createElement('dc:source')
            source.appendChild(doc.createTextNode(self.source))
            metadata.appendChild(source)

        for text in self.languages:
            language = doc.createElement('dc:language')
            language.appendChild(doc.createTextNode(text))
            metadata.appendChild(language)

        if self.relation:
            relation = doc.createElement('dc:relation')
            relation.appendChild(doc.createTextNode(self.relation))
            metadata.appendChild(relation)

        if self.coverage:
            coverage = doc.createElement('dc:coverage')
            coverage.appendChild(doc.createTextNode(self.coverage))
            metadata.appendChild(coverage)

        if self.right:
            right = doc.createElement('dc:rights')
            right.appendChild(doc.createTextNode(self.right))
            metadata.appendChild(right)

        for name, content in self.metas:
            meta = doc.createElement('meta')
            meta.setAttribute('name', name)
            meta.setAttribute('content', content)
            metadata.appendChild(meta)

        return metadata


class Manifest(object):
    
    def __init__(self):
        self.items = []
    
    def append(self, item):
        self.items.append(item)


class ManifestItem(object):
    """Represent an item from the epub's manifest."""

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

    def as_xml_element(self):
        """Return an xml dom Element node."""

        item = minidom.Document().createElement("item")

        item.setAttribute('id', self.id)
        item.setAttribute('href', self.href)
        if self.media_type:
            item.setAttribute('media_type', self.media_type)
        if self.fallback:
            item.setAttribute('fallback', self.fallback)
        if self.required_namespace:
            item.setAttribute('required_namespace', self.required_namespace)
        if self.required_modules:
            item.setAttribute('required_modules', self.required_modules)
        if self.fallback_style:
            item.setAttribute('fallback_style', self.fallback_style)

        return item


class Spine(object):
    
    def __init__(self):
        self.toc = None
        self.itemrefs = []
    
    def append(self, itemref):
        self.itemrefs.append(itemref)


class Guide(object):
    
    def __init__(self):
        self.references = []
    
    def append(self, reference):
        self.references.append(reference)

