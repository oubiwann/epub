# -*- coding: utf-8 -*-

"""
Library to open and read files in the epub version 2.
"""

__author__ = u'Florian Strzelecki <florian.strzelecki@gmail.com>'
__version__ = u'0.2.0'

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
    xml_string = book.zip.read(book.opf_path)
    book.opf = opf.parse_opf(xml_string)
    book.uid = [x for x in book.opf.metadata.identifiers if x[1] == book.opf.uid_id][0]
    item_toc = book.get_item(book.opf.spine.toc)
    
    # Inspect NCX toc file
    book.toc = ncx.parse_toc(book.read(item_toc))

    return book


class EpubFile(object):
    """Represents an epub file as described in version 2.0.1
    
    See http://idpf.org/epub/201"""

    def __init__(self, zip=None):
        self.zip = zip
        self.opf_path = None
        self.opf = opf.Opf()
        self.uid = None
        self.toc = ncx.Ncx()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    #
    # Manifest, spine & guide
    #

    def get_item(self, id):
        """Get an item from manifest through its "id" attribute.
        
        Return an EpubManifestItem if found, else None."""
        l = [x for x in self.opf.manifest.items if x.id == id]
        if l:
            return l[0]
        else:
            return None

    def get_item_by_href(self, href):
        """Get an item from manifest through its "href" attribute.
        
        Return an EpubManifestItem if found, else None."""
        l = [x for x in self.opf.manifest.items if x.href == href]
        if l:
            return l[0]
        else:
            return None

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

