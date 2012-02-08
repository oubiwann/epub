# -*- coding: utf-8 -*-

"""
Library to open and read files in the epub version 2.
"""

__author__ = u'Florian Strzelecki <florian.strzelecki@gmail.com>'
__version__ = u'0.1.1'

import os
import zipfile

from xml.dom import minidom

from epub import ncx, opf

MIMETYPE_OPF = u'application/oebps-package+xml'
MIMETYPE_NCX = u'application/x-dtbncx+xml'

def open(filename):
    """Open an epub file and return an EpubFile object

    File is opened read-only.
    """
    book = EpubFile(zip=zipfile.ZipFile(filename))

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
    for node in [e for e in package.childNodes if e.nodeType == e.ELEMENT_NODE]:
        data[node.tagName.lower()] = node

    # Inspect metadata
    book.metadata = opf._parse_xml_metadata(data['metadata'])

    # Get Uid
    book.uid_id = package.getAttribute('unique-identifier')
    book.uid = [x for x in book.metadata.identifier if x[1] == book.uid_id][0]

    # Inspect manifest
    book.manifest = opf._parse_xml_manifest(data['manifest'])

    # Inspect spine
    item_toc = book.get_item(data['spine'].getAttribute('toc'))
    book.spine = opf._parse_xml_spine(data['spine'])

    # Inspect guide if exist
    if 'guide' in data:
        book.guide = opf._parse_xml_guide(data['guide'])

    # Inspect NCX toc file
    book.toc = ncx.parse_toc(book.read(item_toc))

    return book


class EpubFile(object):
    """Represents an epub file as described in version 2.0.1
    
    See http://idpf.org/epub/201"""

    def __init__(self, zip=None):
        self.zip = zip
        self.opf_path = None
        self.uid = None
        self.uid_id = None
        self.metadata = None
        self.manifest = []
        self.spine = []
        self.guide = []
        self.toc = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    #
    # Manifest, spine & guide
    #

    def add_item(self, id, href, media_type=None, fallback=None, 
                 required_namespace=None, required_modules=None, 
                 fallback_style=None):
        item = opf.ManifestItem(id, href, media_type,
                                fallback, required_namespace, required_modules,
                                fallback_style)
        self.manifest.append(item)

    def add_spine_itemref(self, idref, linear=True):
        self.spine.append((idref, linear))

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
        if isinstance(item, opf.ManifestItem):
            path = item.href
        dirpath = os.path.dirname(self.opf_path)
        return self.zip.read(os.path.join(dirpath, path))

    def close(self):
        """Close the zipfile archive.
        
        Not very usefull yet, because zipfile is open in read-only."""
        self.zip.close()

