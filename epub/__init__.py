# -*- coding: utf-8 -*-

"""
Library to open and read files in the epub version 2.
"""

__author__ = u'Florian Strzelecki <florian.strzelecki@gmail.com>'
__version__ = u'0.3.0'

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
    book = EpubFile(filename, mode=u'r')
    
    # Read container.xml to get OPF xml file path
    xmlstring = book.read_file('META-INF/container.xml')
    container_xml = minidom.parseString(xmlstring).documentElement
    
    for e in container_xml.getElementsByTagName('rootfile'):
        if e.getAttribute('media-type') == MIMETYPE_OPF:
            book.opf_path = e.getAttribute('full-path')
            break
    
    # Read OPF xml file
    xml_string = book.read_file(book.opf_path)
    book.opf = opf.parse_opf(xml_string)
    book.uid = [x for x in book.opf.metadata.identifiers if x[1] == book.opf.uid_id][0]
    item_toc = book.get_item(book.opf.spine.toc)
    
    # Inspect NCX toc file
    book.toc = ncx.parse_toc(book.read(item_toc))

    return book


class EpubFile(zipfile.ZipFile):
    """Represent an epub zip file, as described in version 2.0.1 of epub spec.
    
    This class allow an access throught a low-level API to the epub real file.
    It extends zipfile.ZipFile class and modify only a little some of its 
    behavior.
    
    See http://idpf.org/epub/201 for more information about Epub 2.0.1."""

    def __init__(self, file, mode=u'r', compression=0, allowZip64=False):
        """Open the Epub zip file with mode read "r", write "w" or append "a".
        TODO: check if file is a real epub file if opened with "r" or "a" mode.
        In "a" mode, an empty file is valid (as in "w" mode), but it may not 
        be valid if not empty.
        TODO: in "w" mode, create and add a "mimetype" file within the archive
        TODO: in "a" mode, if zipfile is empty, act as in "w" mode
        """
        zipfile.ZipFile.__init__(self, file, mode, compression, allowZip64)
        self.opf_path = None
        self.opf = opf.Opf()
        self.uid = None
        self.toc = ncx.Ncx()

    #
    # Manifest, spine & guide
    #

    def get_item(self, id):
        """Get an item from manifest through its "id" attribute.
        
        Return an EpubManifestItem if found, else None."""
        return self.opf.manifest.get(id, None)

    def get_item_by_href(self, href):
        """Get an item from manifest through its "href" attribute.
        
        Return an EpubManifestItem if found, else None."""
        l = [x for x in self.opf.manifest.values() if x.href == href]
        size = len(l)
        if size == 1:
            return l[0]
        elif size > 1:
            raise LookupError(u'Multiple items are found with this href.')
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
        return self.read_file(os.path.join(dirpath, path))

    def read_file(self, path):
        return zipfile.ZipFile.read(self, path)

