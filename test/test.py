# -*- coding: utf-8 -*-

import os
import unittest
import epub

from xml.dom import minidom

class TestEpubOpen(unittest.TestCase):
    epub_path = '_data/test.epub'

    def test_open(self):
        test_path = os.path.join(os.path.dirname(__file__), self.epub_path)
        book = epub.open(test_path)
        
        self.assertEqual(book.opf.metadata.languages, ['en',])
        self.assertEqual(book.opf.metadata.titles, [(u'Testing Epub', ''),])
        self.assertEqual(len(book.opf.manifest.items), 7)
        for item in book.opf.manifest.items:
            self.assertIsInstance(item, epub.opf.ManifestItem)

    def test_parse_xml_metadata(self):
        """Test _parse_xml_metadata."""

        xml_string = u"""
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
            <dc:identifier opf:scheme="epub_test" id="epub_id">1</dc:identifier>
            <dc:identifier opf:scheme="uuid" id="uuid_id">18430f16-c687-400b-9b9c-54a9c8b0646c</dc:identifier>
            <dc:title>Metadata for testing purpose</dc:title>
            <dc:title xml:lang="fr">Metadonnée pour les tests.</dc:title>
            <dc:creator opf:file-as="Doe, Jhon" opf:role="aut">John Doe</dc:creator>
            <dc:contributor opf:file-as="Python, unittest" opf:role="other.test">Python unittest</dc:contributor>
            <dc:contributor opf:file-as="Python, nosetests" opf:role="other.test">Python nosetests</dc:contributor>
            <dc:date opf:event="creation">2012-01-05T16:18:00+00:00</dc:date>
            <dc:date opf:event="publication">2012-01-09T13:37:00+00:00</dc:date>
            <dc:publisher>Exirel</dc:publisher>
            <dc:language>en</dc:language>
            <meta content="Custom Meta" name="custom:meta"/>
            <meta content="Another Custom Meta" name="custom:other"/>
        </metadata>
        """
        element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        metadata = epub.opf._parse_xml_metadata(element)
        
        # dc:identifier
        self.assertEqual(metadata.identifiers,
                         [(u'1', u'epub_id', u'epub_test'),
                          (u'18430f16-c687-400b-9b9c-54a9c8b0646c', u'uuid_id', u'uuid')])
        
        # dc:title
        self.assertEqual(metadata.titles,
                         [(u'Metadata for testing purpose', ''),
                          (u'Metadonnée pour les tests.', 'fr')])
        
        # dc:creator
        self.assertEqual(metadata.creators,
                         [(u'John Doe', u'aut', u'Doe, Jhon'),])
        
        # dc:contributor
        self.assertEqual(metadata.contributors,
                         [(u'Python unittest', u'other.test', u'Python, unittest'),
                          (u'Python nosetests', u'other.test', u'Python, nosetests')])
        
        # dc:date
        self.assertEqual(metadata.dates,
                         [(u'2012-01-05T16:18:00+00:00', u'creation'),
                          (u'2012-01-09T13:37:00+00:00', u'publication')])
        
        # dc:publisher
        self.assertEqual(metadata.publisher, u'Exirel')
        
        # dc:language
        self.assertEqual(metadata.languages,
                         [u'en',])
        
        # meta
        self.assertEqual(metadata.metas,
                         [(u'custom:meta', u'Custom Meta'),
                          (u'custom:other', u'Another Custom Meta')])

    def test_parse_xml_manifest(self):
        xml_string = """
        <manifest>
            <notAnItem id="fake" href="fake.fk" media-type="plain/text" />
            <item id="toc" href="toc.ncx" media-type="application/x-dtbncx+xml" />
            <item id="cover" href="Text/cover.html" media-type="application/xhtml+xml" />
            <item id="chap1" href="Text/chap1.html" media-type="application/xhtml+xml" />
            <item id="chap2" href="Text/chap2.html" media-type="application/xhtml+xml" />
        </manifest>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        manifest = epub.opf._parse_xml_manifest(xml_element)
        self.assertIsInstance(manifest, epub.opf.Manifest,
                              u'Manifest must be an epub.opf.Manifest instance.')
        self.assertEqual(len(manifest.items), 4)
        
        for item in manifest.items:
            self.assertIsInstance(item, epub.opf.ManifestItem)
        
        self.assertEqual(manifest.items[0].id, u'toc')
        self.assertEqual(manifest.items[1].id, u'cover')
        self.assertEqual(manifest.items[2].id, u'chap1')
        self.assertEqual(manifest.items[3].id, u'chap2')
        
        self.assertEqual(manifest.items[0].href, u'toc.ncx')
        self.assertEqual(manifest.items[1].href, u'Text/cover.html')
        self.assertEqual(manifest.items[2].href, u'Text/chap1.html')
        self.assertEqual(manifest.items[3].href, u'Text/chap2.html')


class TestEpubFile(unittest.TestCase):
    """Test class for epub.EpubFile class"""

    epub_file = None

    def setUp(self):
        epub_file = epub.EpubFile()
        manifest = epub.opf.Manifest()
        manifest.items = [epub.opf.ManifestItem('toc', 'toc.ncx', epub.MIMETYPE_NCX),
                    epub.opf.ManifestItem('Chap001', 'Text/chap1.xhtml',
                                          epub.MIMETYPE_OPF),
                    epub.opf.ManifestItem('Chap002', 'Text/chap2.xhtml',
                                          epub.MIMETYPE_OPF),
                    ]
        epub_file.opf = epub.opf.Opf()
        epub_file.opf.manifest = manifest
        self.epub_file  = epub_file

    def test_add_item(self):
        """Check EpubFile.add_item() add an item to the manifest."""
        self.assertEqual(len(self.epub_file.opf.manifest.items), 3,
                         u'Le setup n\'est pas bon')
        self.epub_file.add_item('Chap003', 'Text/chap3.xhtml',
                                epub.MIMETYPE_OPF)
        self.assertEqual(len(self.epub_file.opf.manifest.items), 4,
                         u'Il manque un objet !')

    def test_get_item(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its id"""
        item = self.epub_file.get_item('Chap002')
        self.assertIsInstance(item, epub.opf.ManifestItem,
                              u'L\'item retourné doit être un objet de type <epub.opf.ManifestItem>')
        self.assertEqual(item.id, 'Chap002', u'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/chap2.xhtml',
                         u'href attendu incorrect.')

    def test_get_item_by_ref(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its href"""
        item = self.epub_file.get_item_by_href('Text/chap2.xhtml')
        self.assertIsInstance(item, epub.opf.ManifestItem,
                              u'L\'item retourné doit être un objet de type <epub.opf.ManifestItem>')
        self.assertEqual(item.id, 'Chap002', u'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/chap2.xhtml',
                         u'href attendu incorrect.')

