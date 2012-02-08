# -*- coding: utf-8 -*-

import unittest

from xml.dom import minidom

import epub


class TestFunction(unittest.TestCase):

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


class TestManifest(unittest.TestCase):

    def test_add_item(self):
        """Check epub.opf.Manifest.add_item()"""
        
        manifest = epub.opf.Manifest()
        manifest.items = []
        
        manifest.add_item('Chap003', 'Text/chap3.xhtml', epub.MIMETYPE_OPF)
        self.assertEqual(len(manifest.items), 1,
                         u'Il manque un objet !')
        self.assertIsInstance(manifest.items[0], epub.opf.ManifestItem)

    def test_as_xml_element(self):
        xml_string = u"""<manifest>
    <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
    <item href="Text/introduction.xhtml" id="introduction.xhtml" media-type="application/xhtml+xml"/>
    <item href="Text/cover.xhtml" id="cover.xhtml" media-type="application/xhtml+xml"/>
    <item href="Text/Section0002.xhtml" id="Section0002.xhtml" media-type="application/xhtml+xml"/>
    <item href="Text/Section0001.xhtml" id="Section0001.xhtml" media-type="application/xhtml+xml"/>
    <item href="Text/Section0003.xhtml" id="Section0003.xhtml" media-type="application/xhtml+xml"/>
    <item href="Text/Section0004.xhtml" id="Section0004.xhtml" media-type="application/xhtml+xml"/>
</manifest>"""

        self.maxDiff = None
        doc = minidom.parseString(xml_string)
        xml_element = doc.documentElement
        
        manifest = epub.opf._parse_xml_manifest(xml_element)
        
        self.assertEqual(manifest.as_xml_element().toprettyxml('    ').strip(),
                         xml_element.toxml().strip())


class TestOpf(unittest.TestCase):
    
    def test_as_xml_document(self):
        xml_string = """<?xml version="1.0" ?>
<package unique-identifier="BookId" version="2.0" xmlns="http://www.idpf.org/2007/opf">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:title>
            Testing Epub
        </dc:title>
        <dc:creator opf:role="aut">
            Florian Strzelecki
        </dc:creator>
        <dc:identifier id="BookId" opf:scheme="UUID">
            urn:uuid:477d1a82-a70d-4ee5-a0ff-0dddc60fd2bb
        </dc:identifier>
        <dc:language>
            en
        </dc:language>
        <meta content="0.4.2" name="Sigil version"/>
    </metadata>
    <manifest>
        <item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
        <item href="Text/introduction.xhtml" id="introduction.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/cover.xhtml" id="cover.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/Section0002.xhtml" id="Section0002.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/Section0001.xhtml" id="Section0001.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/Section0003.xhtml" id="Section0003.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/Section0004.xhtml" id="Section0004.xhtml" media-type="application/xhtml+xml"/>
    </manifest>
    <spine toc="ncx">
        <itemref idref="cover.xhtml"/>
        <itemref idref="introduction.xhtml"/>
        <itemref idref="Section0001.xhtml"/>
        <itemref idref="Section0002.xhtml"/>
        <itemref idref="Section0003.xhtml"/>
        <itemref idref="Section0004.xhtml"/>
    </spine>
    <guide>
        <reference href="Text/introduction.xhtml" title="Preface" type="preface"/>
        <reference href="Text/cover.xhtml" title="Cover" type="cover"/>
        <reference href="Text/Section0001.xhtml" title="Text" type="text"/>
        <reference href="Text/Section0002.xhtml" title="Text" type="text"/>
        <reference href="Text/Section0003.xhtml" title="Text" type="text"/>
        <reference href="Text/Section0004.xhtml" title="Text" type="text"/>
    </guide>
</package>
"""
        opf = epub.opf.parse_opf(xml_string)
        xml_toc = opf.as_xml_document().toprettyxml('    ')

        self.assertEqual(xml_string, xml_toc)
