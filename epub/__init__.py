# -*- coding: utf-8 -*-
"""
Library to open and read files in the epub version 2.
"""


__author__ = u'Florian Strzelecki <florian.strzelecki@gmail.com>'
__version__ = u'0.5.0'
__all__ = ['opf', 'ncx']


import os
import uuid
import zipfile


from xml.dom import minidom


from epub import ncx, opf


MIMETYPE_EPUB = u'application/epub+zip'
MIMETYPE_OPF = u'application/oebps-package+xml'
MIMETYPE_NCX = u'application/x-dtbncx+xml'

DEFAULT_OPF_PATH = u'OEBPS/content.opf'
DEFAULT_NCX_PATH = u'toc.ncx'


def open(filename, mode=u'r'):
    """Open an epub file and return an EpubFile object"""
    return EpubFile(filename, mode)


class BadEpubFile(zipfile.BadZipfile):
    pass


class EpubFile(zipfile.ZipFile):
    """Represent an epub zip file, as described in version 2.0.1 of epub spec.

    This class allow an access throught a low-level API to the epub real file.
    It extends zipfile.ZipFile class and modify only a little some of its
    behavior.

    See http://idpf.org/epub/201 for more information about Epub 2.0.1."""

    @property
    def content_path(self):
        """Return the content path, ie, the path relative to OPF file.

        If OPF file is located in `OEBPS/content.opf`, then `content_path` is
        equal to `OEBPS`.
        """
        return os.path.dirname(self.opf_path)

    def __init__(self, filename, mode=u'r'):
        """Open the Epub zip file with mode read "r", write "w" or append "a".
        """
        zipfile.ZipFile.__init__(self, filename, mode)

        if self.mode == u'r':
            self._init_read()
        elif self.mode == u'w':
            self._init_new()
        elif self.mode == u'a':
            if len(self.namelist()) == 0:
                self._init_new()
            else:
                self._init_read()

    def _init_new(self):
        """Build an empty epub archive."""
        # Write mimetype file: 'application/epub+zip'
        self.writestr(u'mimetype', MIMETYPE_EPUB)
        # Default path for opf
        self.opf_path = DEFAULT_OPF_PATH
        # Uid & Uid's id
        uid_id = u'BookId'
        self.uid = u'%s' % uuid.uuid4()
        # Create metadata, manifest, and spine, as minimalist as possible
        metadata = opf.Metadata()
        metadata.add_identifier(self.uid, uid_id, u'uid')
        manifest = opf.Manifest()
        manifest.add_item(u'ncx', u'toc.ncx', MIMETYPE_NCX)
        spine = opf.Spine(u'ncx')
        # Create Opf object
        self.opf = opf.Opf(uid_id=uid_id,
                           metadata=metadata, manifest=manifest, spine=spine)
        # Create Ncx object
        self.toc = ncx.Ncx()
        self.toc.uid = self.uid

    def _init_read(self):
        # Read container.xml to get OPF xml file path
        xmlstring = self.read(u'META-INF/container.xml')
        container_xml = minidom.parseString(xmlstring).documentElement

        for e in container_xml.getElementsByTagName(u'rootfile'):
            if e.getAttribute(u'media-type') == MIMETYPE_OPF:
                # Only take the first full-path available
                self.opf_path = e.getAttribute(u'full-path')
                break

        # Read OPF xml file
        xml_string = self.read(self.opf_path)
        self.opf = opf.parse_opf(xml_string)
        self.uid = [x for x in self.opf.metadata.identifiers if x[1] == self.opf.uid_id][0]
        item_toc = self.get_item(self.opf.spine.toc)

        # Inspect NCX toc file
        self.toc = ncx.parse_toc(self.read_item(item_toc))

    def close(self):
        if self.fp is None:
            return
        if self.mode in (u'w', u'a'):
            self._write_close()
        zipfile.ZipFile.close(self)

    def _write_close(self):
        """Handle writes when closing epub. Both new file mode (w) and append
        file mode (a), some files must be generated: container, OPF, and NCX.
        """
        # Write META-INF/container.xml
        self.writestr(u'META-INF/container.xml',
                      self._build_container().encode(u'utf-8'))
        # Write OPF File
        self.writestr(self.opf_path,
                      self.opf.as_xml_document().toxml().encode(u'utf-8'))
        # Write NCX File
        item_toc = self.get_item(self.opf.spine.toc)
        self.writestr(os.path.join(self.content_path, item_toc.href),
                      self.toc.as_xml_document().toxml().encode(u'utf-8'))

    def _build_container(self):
        template = u"""<?xml version="1.0" encoding="UTF-8"?>
    <container version="1.0"
               xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
        <rootfiles>
             <rootfile full-path="%s"
                       media-type="application/oebps-package+xml"/>
        </rootfiles>
    </container>"""
        return template % self.opf_path

    def add_item(self, filename, manifest_item,
                 append_to_spine=False, is_linear=True):
        """
        Add a file to epub. A manifest item must be provide to describe it.
        This function will raise a RuntimeError if epub is already closed. It
        will raise an IOError if epub is open in read-only (`r` mode).

        Optional: you can use `append_to_spine` flag (default=False) to append
        item to spine, and use `is_linear` (default=True) to specify if it is
        linear or not.
        """
        self.check_mode_write()
        self.opf.manifest.append(manifest_item)
        self.write(filename, os.path.join(self.content_path,
                                          manifest_item.href))
        if append_to_spine:
            self.opf.spine.add_itemref(manifest_item.identifier, is_linear)

    def check_mode_write(self):
        """
        Raise error if epub file is not writable.

        Raise RuntimeError if file is already closed.

        Raise IOError if file is opened read-only.
        """
        if not self.fp:
            raise RuntimeError(
                  u'Attempt to write to EPUB file that was already closed')

        if self.mode == u'r':
            raise IOError(
                  u'Attempt to write to EPUB file that was open as read-only.')

    def get_item(self, identifier):
        """Get an item from manifest through its "id" attribute.

        Return an EpubManifestItem if found, else None."""
        return self.opf.manifest.get(identifier, None)

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

    # read method is zipfile.ZipFile.read(path)

    def read_item(self, item):
        """Read a file from the epub zipfile container.

        "item" parameter can be the relative path to the opf file or an
        EpubManifestItem object.

        Html fragments are not acceptable : the path must be exactly the same
        as indicated in the opf file.
        """
        path = item
        if hasattr(item, u'href'):
            path = item.href
        return self.read(os.path.join(self.content_path, path))
