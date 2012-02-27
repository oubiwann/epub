# -*- coding: utf-8 -*-

import unittest

from xml.dom import minidom

import epub


class TestFunction(unittest.TestCase):

    def test_parse_opf(self):
        xml_string = u"""<?xml version="1.0" ?>
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
</package>
"""
        opf = epub.opf.parse_opf(xml_string)
        self.assertIsInstance(opf.metadata, epub.opf.Metadata)
        self.assertIsInstance(opf.manifest, epub.opf.Manifest)
        self.assertIsInstance(opf.guide, epub.opf.Guide)
        self.assertIsInstance(opf.spine, epub.opf.Spine)

    def test_parse_xml_metadata(self):
        """Test _parse_xml_metadata."""
        
        xml_string = u"""
        <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
            <dc:identifier opf:scheme="epub_test" id="epub_id">
                1
            </dc:identifier>
            <dc:identifier opf:scheme="uuid" id="uuid_id">
                18430f16-c687-400b-9b9c-54a9c8b0646c
            </dc:identifier>
            <dc:title>
                Metadata for testing purpose
            </dc:title>
            <dc:title xml:lang="fr">
                Metadonnée pour les tests.
            </dc:title>
            <dc:creator opf:file-as="Doe, Jhon" opf:role="aut">
                John Doe
            </dc:creator>
            <dc:subject>
                This is an arbitrary subjet.
            </dc:subject>
            <dc:subject>
                Another usefull subject.
            </dc:subject>
            <dc:contributor opf:file-as="Python, unittest" opf:role="other.test">
                Python unittest
            </dc:contributor>
            <dc:contributor opf:file-as="Python, nosetests" opf:role="other.test">
                Python nosetests
            </dc:contributor>
            <dc:description>
                A long description. There is not any information about how a 
                description must be. Long, short, etc.
                
                We just don't know anything about this.
            </dc:description>
            <dc:date opf:event="creation">
                2012-01-05T16:18:00+00:00
            </dc:date>
            <dc:date opf:event="publication">
                2012-01-09T13:37:00+00:00
            </dc:date>
            <dc:type>
                Is this a type?
            </dc:type>
            <dc:format>
               Well formated, sir!
            </dc:format>
            <dc:publisher>
                Exirel
            </dc:publisher>
            <dc:language>
                en
            </dc:language>
            <dc:source>
                From the far old west (Brittany, France).
            </dc:source>
            <dc:relation>
                It's complicated...
            </dc:relation>
            <dc:coverage>
                An art of cover.
            </dc:coverage>
            <dc:rights>
                To the left!
            </dc:rights>
            <meta content="Custom Meta" name="custom:meta"/>
            <meta content="Another Custom Meta" name="custom:other"/>
        </metadata>
        """
        element = minidom.parseString(xml_string.encode(u'utf-8')).documentElement
        metadata = epub.opf._parse_xml_metadata(element)
        
        # dc:identifier
        self.assertEqual(metadata.identifiers,
                         [(u'1', u'epub_id', u'epub_test'),
                          (u'18430f16-c687-400b-9b9c-54a9c8b0646c', u'uuid_id', u'uuid')])
        
        # dc:title
        self.assertEqual(metadata.titles,
                         [(u'Metadata for testing purpose', ''),
                          (u'Metadonnée pour les tests.', u'fr')])
        
        # dc:creator
        self.assertEqual(metadata.creators,
                         [(u'John Doe', u'aut', u'Doe, Jhon'),])
        
        # dc:subject
        self.assertEqual(metadata.subjects,
                         [u'This is an arbitrary subjet.',
                          u'Another usefull subject.'])
        
        # dc:description
        self.assertEqual(metadata.description,
                         u"""A long description. There is not any information about how a 
                description must be. Long, short, etc.
                
                We just don't know anything about this.""")
        
        # dc:contributor
        self.assertEqual(metadata.contributors,
                         [(u'Python unittest', u'other.test', u'Python, unittest'),
                          (u'Python nosetests', u'other.test', u'Python, nosetests')])
        
        # dc:date
        self.assertEqual(metadata.dates,
                         [(u'2012-01-05T16:18:00+00:00', u'creation'),
                          (u'2012-01-09T13:37:00+00:00', u'publication')])
        
        # dc:type
        self.assertEqual(metadata.type, u'Is this a type?')
        
        # dc:format
        self.assertEqual(metadata.format, u'Well formated, sir!')
        
        # dc:publisher
        self.assertEqual(metadata.publisher, u'Exirel')
        
        # dc:language
        self.assertEqual(metadata.languages,
                         [u'en',])
        
        # dc:source
        self.assertEqual(metadata.source,
                         u'From the far old west (Brittany, France).')
        
        # dc:relation
        self.assertEqual(metadata.relation,
                         u'It\'s complicated...')
        
        # dc:coverage
        self.assertEqual(metadata.coverage,
                         u'An art of cover.')
        
        # dc:rights
        self.assertEqual(metadata.right,
                         u'To the left!')
        # meta
        self.assertEqual(metadata.metas,
                         [(u'custom:meta', u'Custom Meta'),
                          (u'custom:other', u'Another Custom Meta')])

    def test_parse_xml_manifest(self):
        xml_string = u"""
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
        self.assertEqual(len(manifest), 4)
        
        for key, item in manifest.iteritems():
            self.assertIsInstance(item, epub.opf.ManifestItem)
        
        self.assertEqual(manifest[u'toc'].id, u'toc')
        self.assertEqual(manifest[u'cover'].id, u'cover')
        self.assertEqual(manifest[u'chap1'].id, u'chap1')
        self.assertEqual(manifest[u'chap2'].id, u'chap2')
        
        self.assertEqual(manifest[u'toc'].href, u'toc.ncx')
        self.assertEqual(manifest[u'cover'].href, u'Text/cover.html')
        self.assertEqual(manifest[u'chap1'].href, u'Text/chap1.html')
        self.assertEqual(manifest[u'chap2'].href, u'Text/chap2.html')


class TestMetadata(unittest.TestCase):
    
    def test_add_identifier(self):
        metadata = epub.opf.Metadata()
        self.assertEqual(metadata.identifiers, [])
        
        metadata.add_identifier(u'978-284172074-3', u'ID_ISBN', u'isbn')
        
        self.assertEqual(metadata.identifiers,
                         [(u'978-284172074-3', u'ID_ISBN', u'isbn')])
        
        metadata.add_identifier(u'781445645135453123543', u'ID_UID', u'UID')
        
        self.assertEqual(metadata.identifiers,
                         [(u'978-284172074-3', u'ID_ISBN', u'isbn'),
                          (u'781445645135453123543', u'ID_UID', u'UID')])
        
    def test_get_isbn(self):
        metadata = epub.opf.Metadata()
        self.assertEqual(metadata.get_isbn(), None)
        
        metadata.add_identifier(u'978-284172074-3', u'ID_ISBN', u'isbn')
        metadata.add_identifier(u'781445645135453123543', u'ID_UID', u'UID')
        
        self.assertEqual(metadata.get_isbn(), u'978-284172074-3')

    def test_as_xml_element(self):
        xml_string = u"""<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title xml:lang="fr">
        Le titre.
    </dc:title>
    <dc:title xml:lang="en">
        The title.
    </dc:title>
</metadata>"""

        self.maxDiff = None
        doc = minidom.parseString(xml_string)
        xml_element = doc.documentElement
        
        metadata = epub.opf._parse_xml_metadata(xml_element)
        
        self.assertEqual(metadata.as_xml_element().toprettyxml(u'    ').strip(),
                         xml_element.toxml().strip())


class TestManifest(unittest.TestCase):

    class TestDuckManifestItem(object):
        
        def __init__(self, id=None, href=None):
            self.id = id
            if href:
                self.href = href

    def test_dict_behavior(self):
        id = u'ID001'
        bad_id = u'BAD_ID001'
        duck_id = u'FAKE_ID001'
        duck_href = u'fake_item_001.xhtml'
        href = u'item_001.xhtml'
        media = u'application/xhtml+xml'
        manifest = epub.opf.Manifest()
        manifest_item = epub.opf.ManifestItem(id, href, media)
        
        self.assertEqual(len(manifest), 0)
        
        manifest[id] = manifest_item
        
        self.assertEqual(len(manifest), 1)
        self.assertEqual(manifest[id], manifest_item)

        with self.assertRaises(ValueError):
            manifest[bad_id] = manifest_item

        duck_ok = self.TestDuckManifestItem(duck_id, duck_href)
        manifest[duck_id] = duck_ok

        with self.assertRaises(ValueError):
            duck_ko = self.TestDuckManifestItem(duck_id)
            manifest[duck_id] = duck_ko

        with self.assertRaises(ValueError):
            duck_ko = self.TestDuckManifestItem(duck_id)
            manifest.append(duck_ko)

        self.assertTrue(id in manifest)
        self.assertTrue(manifest_item in manifest)
        self.assertTrue(duck_ok in manifest)

    def test_add_item(self):
        """Check epub.opf.Manifest.add_item()"""
        
        id = u'Chap003'
        href = u'Text/chap3.xhtml'
        media_type = epub.MIMETYPE_OPF
        
        manifest = epub.opf.Manifest()
        item = epub.opf.ManifestItem(id, href, media_type)
        
        manifest.add_item(id, href, media_type)
        
        self.assertEqual(len(manifest), 1, u'Il manque un objet !')
        self.assertIsInstance(manifest[id], epub.opf.ManifestItem)

    def test_as_xml_element(self):
        xml_string = u"""<manifest>
    <item id="css1" href="happy.css" media-type="text/css" />
    <item id="item2" href="Doc1.less-hpy" media-type="text/less-happy+xml" required-namespace="http://happy.com/ns/happy2/" fallback="item2.5" fallback-style="css1" />
    <item id="item2.5" href="Doc1.htm" media-type="application/xhtml+xml" required-namespace="http://www.w3.org/1999/xhtml" required-modules="ruby, server-side-image-map" fallback="item3" />
    <item id="item1" href="Doc1.hpy" media-type="text/happy+xml" required-namespace="http://happy.com/ns/happy1/" fallback="item2" />
    <item id="item4" href="Doc2.hpy" media-type="text/happy+xml" required-namespace="http://happy.com/ns/happy1/" fallback-style="css1" />
    <item id="item3" href="Doc1.dtb" media-type="application/x-dtbook+xml" />
</manifest>"""

        self.maxDiff = None
        doc = minidom.parseString(xml_string)
        xml_element = doc.documentElement
        
        manifest = epub.opf._parse_xml_manifest(xml_element)
        
        xml_input = xml_element.toxml().strip()
        xml_output = manifest.as_xml_element().toprettyxml(u'    ').strip()
        
        print xml_input
        print xml_output
        
        self.assertEqual(xml_output, xml_input)


class TestGuide(unittest.TestCase):
    
    def test_as_xml_element(self):
        xml_string = u"""<guide>
    <reference type="toc" title="Table of Contents" href="toc.html" />
    <reference type="loi" title="List Of Illustrations" href="toc.html#figures" />
    <reference type="other.intro" title="Introduction" href="intro.html" />
</guide>"""

        self.maxDiff = None
        doc = minidom.parseString(xml_string)
        xml_element = doc.documentElement
        
        guide = epub.opf._parse_xml_guide(xml_element)
        
        self.assertEqual(guide.as_xml_element().toprettyxml(u'    ').strip(),
                         xml_element.toxml().strip())


class TestSpine(unittest.TestCase):
    
    def test_as_xml_element(self):
        xml_string = u"""<spine toc="ncx">
    <itemref idref="intro" />
    <itemref idref="c1" />
    <itemref idref="c1-answerkey" linear="no" />
    <itemref idref="c2" />
    <itemref idref="c2-answerkey" linear="no" />
    <itemref idref="c3" />
    <itemref idref="c3-answerkey" linear="no" />
    <itemref idref="note" linear="no" />
</spine>"""

        self.maxDiff = None
        doc = minidom.parseString(xml_string)
        xml_element = doc.documentElement
        
        spine = epub.opf._parse_xml_spine(xml_element)
        
        self.assertEqual(spine.as_xml_element().toprettyxml(u'    ').strip(),
                         xml_element.toxml().strip())


class TestOpf(unittest.TestCase):
    
    def test_init(self):
        opf = epub.opf.Opf()
        
        self.assertIsInstance(opf.metadata, epub.opf.Metadata)
        self.assertIsInstance(opf.manifest, epub.opf.Manifest)
        self.assertIsInstance(opf.spine, epub.opf.Spine)
        self.assertIsInstance(opf.guide, epub.opf.Guide)

    def test_as_xml_document(self):
        xml_string = u"""<?xml version="1.0" ?>
<package unique-identifier="BookId" version="2.0" xmlns="http://www.idpf.org/2007/opf">
    <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
        <dc:title xml:lang="en">
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
        <item href="Text/Section0004.xhtml" id="Section0004.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/Section0002.xhtml" id="Section0002.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/Section0001.xhtml" id="Section0001.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/cover.xhtml" id="cover.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/Section0003.xhtml" id="Section0003.xhtml" media-type="application/xhtml+xml"/>
        <item href="Text/introduction.xhtml" id="introduction.xhtml" media-type="application/xhtml+xml"/>
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
        self.maxDiff = None
        opf = epub.opf.parse_opf(xml_string)
        
        xml_input = xml_string.strip()
        xml_output = opf.as_xml_document().toprettyxml(u'    ').strip()
        
        print xml_input
        print xml_output

        self.assertEqual(xml_input, xml_output)
