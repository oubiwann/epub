# -*- coding: utf-8 -*-

import unittest
import epub

from xml.dom import minidom

class TestEpubFile(unittest.TestCase):
    """Test class for epub.EpubFile class"""

    epub_file = None

    def setUp(self):
        epub_file = epub.EpubFile()
        manifest = [epub.EpubManifestItem('toc', 'toc.ncx', epub.MIMETYPE_NCX),
                    epub.EpubManifestItem('Chap001', 'Text/chap1.xhtml',
                                          epub.MIMETYPE_OPF),
                    epub.EpubManifestItem('Chap002', 'Text/chap2.xhtml',
                                          epub.MIMETYPE_OPF),
                    ]
        epub_file.manifest = manifest
        self.epub_file  = epub_file

    def test_add_item(self):
        """Check EpubFile.add_item() add an item to the manifest."""
        self.assertEqual(len(self.epub_file.manifest), 3,
                         u'Le setup n\'est pas bon')
        self.epub_file.add_item('Chap003', 'Text/chap3.xhtml',
                                epub.MIMETYPE_OPF)
        self.assertEqual(len(self.epub_file.manifest), 4,
                         u'Il manque un objet !')

    def test_get_item(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its id"""
        item = self.epub_file.get_item('Chap002')
        self.assertIsInstance(item, epub.EpubManifestItem,
                              u'L\'item retourné doit être un objet de type <EpubManifestItem>')
        self.assertEqual(item.id, 'Chap002', u'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/chap2.xhtml',
                         u'href attendu incorrect.')

    def test_get_item_by_ref(self):
        """Check EpubFile.get_item() return an EpubManifestItem by its href"""
        item = self.epub_file.get_item_by_href('Text/chap2.xhtml')
        self.assertIsInstance(item, epub.EpubManifestItem,
                              u'L\'item retourné doit être un objet de type <EpubManifestItem>')
        self.assertEqual(item.id, 'Chap002', u'id attendu incorrect.')
        self.assertEqual(item.href, 'Text/chap2.xhtml',
                         u'href attendu incorrect.')

class TestEpubMetadata(unittest.TestCase):
    """Test class for epub.EpubMetadata class"""

    element = None

    def setUp(self):
        xml_string = u"""
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
            <dc:identifier opf:scheme="epub_test" id="epub_id">1</dc:identifier>
            <dc:identifier opf:scheme="uuid" id="uuid_id">18430f16-c687-400b-9b9c-54a9c8b0646c</dc:identifier>
            <dc:title>Metadata for testing purpose</dc:title>
            <dc:title xml:lang="fr">Metadonnée pour les tests.</dc:title>
            <dc:creator opf:file-as="Doe, Jhon" opf:role="aut">John Doe</dc:creator>
            <dc:contributor opf:file-as="Python, unittest" opf:role="other.test">Python unittest</dc:contributor>
            <dc:contributor opf:file-as="Python, nosetests" opf:role="other.test">Python nosetests</dc:contributor>
            <dc:date>2012-01-05T16:18:00+00:00</dc:date>
            <dc:publisher>Exirel</dc:publisher>
            <dc:language>en</dc:language>
            <meta content="Custom Meta" name="custom:meta"/>
            <meta content="Another Custom Meta" name="custom:other"/>
        </metadata>
        """
        element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        self.element = element

    def test_set_from_xml(self):
        """Test the behavior of set_from_xml method."""
        metadata = epub.EpubMetadata()
        metadata.set_from_xml(self.element)

        # dc:identifier
        self.assertEqual(metadata.identifier,
                         [(u'1', u'epub_id', u'epub_test'),
                          (u'18430f16-c687-400b-9b9c-54a9c8b0646c', u'uuid_id', u'uuid')])

        # dc:title
        self.assertEqual(metadata.title,
                         [(u'Metadata for testing purpose', ''),
                          (u'Metadonnée pour les tests.', 'fr')])

        # dc:creator
        self.assertEqual(metadata.creator,
                         [(u'John Doe', u'aut', u'Doe, Jhon'),])

        # dc:contributor
        self.assertEqual(metadata.contributor,
                         [(u'Python unittest', u'other.test', u'Python, unittest'),
                          (u'Python nosetests', u'other.test', u'Python, nosetests')])

        # dc:date
        self.assertEqual(metadata.date, u'2012-01-05T16:18:00+00:00')

        # dc:publisher
        self.assertEqual(metadata.publisher, u'Exirel')

        # dc:language
        self.assertEqual(metadata.language,
                         [u'en',])

        # meta
        self.assertEqual(metadata.meta,
                         [(u'custom:meta', u'Custom Meta'),
                          (u'custom:other', u'Another Custom Meta')])



