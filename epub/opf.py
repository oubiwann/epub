# -*- coding: utf-8 -*-

"""
Python lib for reading OPF formated file for epub.

Since the "Tour" element is deprecated in Epub 2, it is not supported by this
library.

OPF epub : http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm
"""
from collections import OrderedDict
from xml.dom import minidom


XMLNS_DC = u'http://purl.org/dc/elements/1.1/'
XMLNS_OPF = u'http://www.idpf.org/2007/opf'


def parse_opf(xml_string):
    package = minidom.parseString(xml_string).documentElement

    # Get Uid
    uid_id = package.getAttribute(u'unique-identifier')

    # Store each child nodes into a dict (metadata, manifest, spine, guide)
    data = {u'metadata': None,
            u'manifest': None,
            u'spine': None,
            u'guide': None}
    elements = [e for e in package.childNodes if e.nodeType == e.ELEMENT_NODE]
    for node in elements:
        data[node.tagName.lower()] = node

    # Inspect metadata
    metadata = _parse_xml_metadata(data[u'metadata'])

    # Inspect manifest
    manifest = _parse_xml_manifest(data[u'manifest'])

    # Inspect spine
    spine = _parse_xml_spine(data[u'spine'])

    # Inspect guide if exist
    if data[u'guide'] is None:
        guide = None
    else:
        guide = _parse_xml_guide(data[u'guide'])

    opf = Opf(uid_id=uid_id,
              metadata=metadata,
              manifest=manifest,
              spine=spine,
              guide=guide)
    return opf


def _parse_xml_metadata(element):
    """Extract metadata from an xml.dom.Element object (ELEMENT_NODE)

    The "<metadata>" tag has a lot of metadatas about the epub this method
    inspect and store into object attributes (like "title" or "creator").
    """
    metadata = Metadata()

    for node in element.getElementsByTagName(u'dc:title'):
        node.normalize()
        metadata.add_title(node.firstChild.data.strip(),
                           node.getAttribute(u'xml:lang'))

    for node in element.getElementsByTagName(u'dc:creator'):
        node.normalize()
        metadata.add_creator(node.firstChild.data.strip(),
                         node.getAttribute(u'opf:role'),
                         node.getAttribute(u'opf:file-as'))

    for node in element.getElementsByTagName(u'dc:subject'):
        node.normalize()
        metadata.add_subject(node.firstChild.data.strip())

    for node in element.getElementsByTagName(u'dc:description'):
        node.normalize()
        metadata.description = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'dc:publisher'):
        node.normalize()
        metadata.publisher = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'dc:contributor'):
        node.normalize()
        metadata.add_contributor(node.firstChild.data.strip(),
                             node.getAttribute(u'opf:role'),
                             node.getAttribute(u'opf:file-as'))

    for node in element.getElementsByTagName(u'dc:date'):
        node.normalize()
        metadata.add_date(node.firstChild.data.strip(),
                          node.getAttribute(u'opf:event'))

    for node in element.getElementsByTagName(u'dc:type'):
        node.normalize()
        metadata.dc_type = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'dc:format'):
        node.normalize()
        metadata.format = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'dc:identifier'):
        node.normalize()
        metadata.add_identifier(node.firstChild.data.strip(),
                            node.getAttribute(u'id'),
                            node.getAttribute(u'opf:scheme'))

    for node in element.getElementsByTagName(u'dc:source'):
        node.normalize()
        metadata.source = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'dc:language'):
        node.normalize()
        metadata.add_language(node.firstChild.data.strip())

    for node in element.getElementsByTagName(u'dc:relation'):
        node.normalize()
        metadata.relation = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'dc:coverage'):
        node.normalize()
        metadata.coverage = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'dc:rights'):
        node.normalize()
        metadata.right = node.firstChild.data.strip()

    for node in element.getElementsByTagName(u'meta'):
        metadata.add_meta(node.getAttribute(u'name'),
                      node.getAttribute(u'content'))

    return metadata


def _parse_xml_manifest(element):
    """Inspect an xml.dom.Element <manifest> and return a list of
    epub.EpubManifestItem object."""

    manifest = Manifest()
    for e in element.getElementsByTagName(u'item'):
        manifest.add_item(e.getAttribute(u'id'),
                          e.getAttribute(u'href'),
                          e.getAttribute(u'media-type'),
                          e.getAttribute(u'fallback'),
                          e.getAttribute(u'required-namespace'),
                          e.getAttribute(u'required-modules'),
                          e.getAttribute(u'fallback-style'))
    return manifest


def _parse_xml_spine(element):
    """Inspect an xml.dom.Element <spine> and return epub.opf.Spine object"""

    spine = Spine()
    spine.toc = element.getAttribute(u'toc')
    for e in element.getElementsByTagName(u'itemref'):
        spine.add_itemref(e.getAttribute(u'idref'),
                          e.getAttribute(u'linear').lower() != u'no')
    return spine


def _parse_xml_guide(element):
    """Inspect an xml.dom.Element <guide> and return a list of ref as tuple."""

    guide = Guide()
    for e in element.getElementsByTagName(u'reference'):
        guide.add_reference(e.getAttribute(u'href'),
                            e.getAttribute(u'type'),
                            e.getAttribute(u'title'))
    return guide


class Opf(object):
    """Represent an OPF formated file.

    OPF is an xml formated file, used in the epub spec."""

    def __init__(self, uid_id=None, version=u'2.0', xmlns=XMLNS_OPF,
                 metadata=None, manifest=None, spine=None, guide=None):
        self.uid_id = uid_id
        self.version = version
        self.xmlns = xmlns

        if metadata is None:
            self.metadata = Metadata()
        else:
            self.metadata = metadata
        if manifest is None:
            self.manifest = Manifest()
        else:
            self.manifest = manifest
        if spine is None:
            self.spine = Spine()
        else:
            self.spine = spine
        if guide is None:
            self.guide = Guide()
        else:
            self.guide = guide

    def as_xml_document(self):
        doc = minidom.Document()
        package = doc.createElement(u'package')
        package.setAttribute(u'version', self.version)
        package.setAttribute(u'unique-identifier', self.uid_id)
        package.setAttribute(u'xmlns', self.xmlns)
        package.appendChild(self.metadata.as_xml_element())
        package.appendChild(self.manifest.as_xml_element())
        package.appendChild(self.spine.as_xml_element())
        package.appendChild(self.guide.as_xml_element())
        doc.appendChild(package)
        return doc


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
        self.dc_type = None
        self.format = None
        self.identifiers = []
        self.source = None
        self.languages = []
        self.relation = None
        self.coverage = None
        self.right = None
        self.metas = []

    def add_title(self, title, lang=u''):
        self.titles.append((title, lang))

    def add_creator(self, name, role=u'aut', file_as=u''):
        self.creators.append((name, role, file_as))

    def add_subject(self, subject):
        self.subjects.append(subject)

    def add_contributor(self, name, role=u'oth', file_as=u''):
        self.contributors.append((name, role, file_as))

    def add_date(self, date, event=u''):
        self.dates.append((date, event))

    def add_identifier(self, content, identifier=u'', scheme=u''):
        self.identifiers.append((content, identifier, scheme))

    def add_language(self, lang):
        self.languages.append(lang)

    def add_meta(self, name, content):
        self.metas.append((name, content))

    def get_isbn(self):
        l = [x[0] for x in self.identifiers if x[2].lower() == u'isbn']
        isbn = None
        if l:
            isbn = l[0]
        return isbn

    def as_xml_element(self):
        """Return an xml dom Element node."""
        doc = minidom.Document()
        metadata = doc.createElement(u'metadata')
        metadata.setAttribute(u'xmlns:dc', XMLNS_DC)
        metadata.setAttribute(u'xmlns:opf', XMLNS_OPF)

        for text, lang in self.titles:
            title = doc.createElement(u'dc:title')
            if lang:
                title.setAttribute(u'xml:lang', lang)
            title.appendChild(doc.createTextNode(text))
            metadata.appendChild(title)

        for name, role, file_as in self.creators:
            creator = doc.createElement(u'dc:creator')
            if role:
                creator.setAttribute(u'opf:role', role)
            if file_as:
                creator.setAttribute(u'opf:file-as', file_as)
            creator.appendChild(doc.createTextNode(name))
            metadata.appendChild(creator)

        for text in self.subjects:
            subject = doc.createElement(u'dc:subject')
            subject.appendChild(doc.createTextNode(text))
            metadata.appendChild(subject)

        if self.description:
            description = doc.createElement(u'dc:description')
            description.appendChild(doc.createTextNode(self.description))
            metadata.appendChild(description)

        if self.publisher:
            publisher = doc.createElement(u'dc:publisher')
            publisher.appendChild(doc.createTextNode(self.publisher))
            metadata.appendChild(publisher)

        for name, role, file_as in self.contributors:
            contributor = doc.createElement(u'dc:contributor')
            if role:
                contributor.setAttribute(u'opf:role', role)
            if file_as:
                contributor.setAttribute(u'opf:file-as', file_as)
            contributor.appendChild(doc.createTextNode(name))
            metadata.appendChild(contributor)

        for text, event in self.dates:
            date = doc.createElement(u'dc:date')
            if event:
                date.setAttribute(u'opf:event', event)
            date.appendChild(doc.createTextNode(text))
            metadata.appendChild(date)

        if self.dc_type:
            dc_type = doc.createElement(u'dc:type')
            dc_type.appendChild(doc.createTextNode(self.dc_type))
            metadata.appendChild(dc_type)

        if self.format:
            dc_format = doc.createElement(u'dc:format')
            dc_format.appendChild(doc.createTextNode(self.format))
            metadata.appendChild(dc_format)

        for text, identifier, scheme in self.identifiers:
            dc_identifier = doc.createElement(u'dc:identifier')
            if identifier:
                dc_identifier.setAttribute(u'id', identifier)
            if scheme:
                dc_identifier.setAttribute(u'opf:scheme', scheme)
            dc_identifier.appendChild(doc.createTextNode(text))
            metadata.appendChild(dc_identifier)

        if self.source:
            source = doc.createElement(u'dc:source')
            source.appendChild(doc.createTextNode(self.source))
            metadata.appendChild(source)

        for text in self.languages:
            language = doc.createElement(u'dc:language')
            language.appendChild(doc.createTextNode(text))
            metadata.appendChild(language)

        if self.relation:
            relation = doc.createElement(u'dc:relation')
            relation.appendChild(doc.createTextNode(self.relation))
            metadata.appendChild(relation)

        if self.coverage:
            coverage = doc.createElement(u'dc:coverage')
            coverage.appendChild(doc.createTextNode(self.coverage))
            metadata.appendChild(coverage)

        if self.right:
            right = doc.createElement(u'dc:rights')
            right.appendChild(doc.createTextNode(self.right))
            metadata.appendChild(right)

        for name, content in self.metas:
            meta = doc.createElement(u'meta')
            meta.setAttribute(u'name', name)
            meta.setAttribute(u'content', content)
            metadata.appendChild(meta)

        return metadata


class Manifest(OrderedDict):

    def __contains__(self, item):
        if hasattr(item, u'identifier'):
            return super(Manifest, self).__contains__(item.identifier)
        else:
            return super(Manifest, self).__contains__(item)

    def __setitem__(self, key, value):
        if hasattr(value, u'identifier') and hasattr(value, u'href'):
            if value.identifier == key:
                super(Manifest, self).__setitem__(key, value)
            else:
                raise ValueError(u'Value\'s id is different from insert key.')
        else:
            requierements = u'id and href attributes'
            msg = u'Value does not fit the requirement (%s).' % requierements
            raise ValueError(msg)

    def add_item(self, identifier, href, media_type=None, fallback=None,
                 required_namespace=None, required_modules=None,
                 fallback_style=None):
        item = ManifestItem(identifier, href, media_type,
                            fallback, required_namespace, required_modules,
                            fallback_style)
        self.append(item)

    def append(self, item):
        self.__setitem__(item.identifier, item)

    def as_xml_element(self):
        """Return an xml dom Element node."""
        doc = minidom.Document()
        manifest = doc.createElement(u'manifest')

        for item in self.itervalues():
            manifest.appendChild(item.as_xml_element())

        return manifest


class ManifestItem(object):
    """Represent an item from the epub's manifest."""

    def __init__(self, identifier, href, media_type=None, fallback=None,
                 required_namespace=None, required_modules=None,
                 fallback_style=None):
        self.identifier = identifier
        self.href = href
        self.media_type = media_type
        self.fallback = fallback
        self.required_namespace = required_namespace
        self.required_modules = required_modules
        self.fallback_style = fallback_style

    def as_xml_element(self):
        """Return an xml dom Element node."""

        item = minidom.Document().createElement(u"item")

        item.setAttribute(u'id', self.identifier)
        item.setAttribute(u'href', self.href)
        if self.media_type:
            item.setAttribute(u'media-type', self.media_type)
        if self.fallback:
            item.setAttribute(u'fallback', self.fallback)
        if self.required_namespace:
            item.setAttribute(u'required-namespace', self.required_namespace)
        if self.required_modules:
            item.setAttribute(u'required-modules', self.required_modules)
        if self.fallback_style:
            item.setAttribute(u'fallback-style', self.fallback_style)

        return item


class Spine(object):

    def __init__(self, toc=None, itemrefs=None):
        self.toc = toc
        if itemrefs is None:
            self.itemrefs = []
        else:
            self.itemrefs = itemrefs

    def add_itemref(self, idref, linear=True):
        self.append((idref, linear))

    def append(self, itemref):
        self.itemrefs.append(itemref)

    def as_xml_element(self):
        doc = minidom.Document()
        spine = doc.createElement(u'spine')
        spine.setAttribute(u'toc', self.toc)

        for idref, linear in self.itemrefs:
            itemref = doc.createElement(u'itemref')
            itemref.setAttribute(u'idref', idref)
            if not linear:
                itemref.setAttribute(u'linear', u'no')
            spine.appendChild(itemref)

        return spine


class Guide(object):

    def __init__(self):
        self.references = []

    def add_reference(self, href, ref_type=None, title=None):
        self.append((href, ref_type, title))

    def append(self, reference):
        self.references.append(reference)

    def as_xml_element(self):
        doc = minidom.Document()
        guide = doc.createElement(u'guide')

        for href, ref_type, title in self.references:
            reference = doc.createElement(u'reference')
            if type:
                reference.setAttribute(u'type', ref_type)
            if title:
                reference.setAttribute(u'title', title)
            if href:
                reference.setAttribute(u'href', href)
            guide.appendChild(reference)

        return guide
