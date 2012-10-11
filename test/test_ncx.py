# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import os
import unittest


from xml.dom import minidom


import epub


class TestFunction(unittest.TestCase):
    """Test case for all the _parse_* function."""

    ncx_path = '_data/test.ncx'

    def test_parse_toc(self):
        test_path = os.path.join(os.path.dirname(__file__), self.ncx_path)
        doc = minidom.parse(test_path)
        xml_string = doc.toprettyxml()
        toc = epub.ncx.parse_toc(xml_string)

        self.assertEqual(toc.xmlns,
                         'http://www.daisy.org/z3986/2005/ncx/')
        self.assertEqual(toc.version,
                         '2005-1')
        self.assertEqual(toc.lang, 'en-US')
        self.assertEqual(toc.title,
                         'Selections from "Great Pictures, As Seen and Described by Famous Writers"')
        self.assertEqual(toc.authors,
                         ['Esther Singleton',
                          'Test Author'])
        self.assertEqual(toc.uid,
                         'org-example-5059463624137734586')
        # nav map
        self.assertIsInstance(toc.nav_map, epub.ncx.NavMap)
        self.assertEqual(len(toc.nav_map.nav_point), 2,
                         'Il manque des nav_point !')
        # page list
        self.assertIsInstance(toc.page_list, epub.ncx.PageList)
        self.assertEqual(len(toc.page_list.page_target), 2,
                         'Il manque des page_target !')
        # nav list
        self.assertEqual(len(toc.nav_lists), 1,
                         'Il manque des nav_list !')
        self.assertIsInstance(toc.nav_lists[0], epub.ncx.NavList)
        self.assertEqual(len(toc.nav_lists[0].nav_target), 2,
                         'Il manque des page_target !')

    def test_parse_for_text_tag(self):
        """Test function "_parse_for_text_tag"."""

        xml_string = """
        <someTag>
            <text>La balise "text" par défaut.</text>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element)
        self.assertEqual(text, 'La balise "text" par défaut.')

        xml_string = """
        <someTag>
            <otherTag>La balise "otherTag" par le paramètre "name".</otherTag>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element, 'otherTag')
        self.assertEqual(text, 'La balise "otherTag" par le paramètre "name".')

        xml_string = """
        <someTag>
            <text>Mauvaise balise !</text>
            <textOk>Bonne balise !</textOk>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element, 'textOk')
        self.assertEqual(text, 'Bonne balise !')

        xml_string = """
        <someTag>
            <text>Première balise uniquement...</text>
            <text>Pas la seconde !</text>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element)
        self.assertEqual(text, 'Première balise uniquement...')

        xml_string = """
        <someTag>
            <text>Je ne cherche pas "text" !</text>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element, 'noText')
        self.assertEqual(text, '', 'Il ne devrait pas y avoir de résultat !')

        xml_string = """
        <someTag>
            <text>
                Du texte avec espace et retour à la ligne.
            </text>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element)
        self.assertEqual(text, 'Du texte avec espace et retour à la ligne.',
                         'Il ne devrait pas y avoir de différence !')

        xml_string = """
        <someTag>
            <emptyText />
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element, 'emptyText')
        self.assertEqual(text, '')

        xml_string = """
        <someTag>
            <emptyText></emptyText>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        text = epub.ncx._parse_for_text_tag(xml_element, 'emptyText')
        self.assertEqual(text, '')

    def test_parse_xml_nav_target(self):
        """Test function "_parse_xml_nav_target"."""

        xml_string = """
        <navTarget playOrder="5"
                   id="part1_target-fragment"
                   value="5"
                   class="some_class">
            <navLabel><text>Label de la Target</text></navLabel>
            <content src="Text/part1.xhtml#target-fragment" />
        </navTarget>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_target = epub.ncx._parse_xml_nav_target(xml_element)
        self.assertIsInstance(nav_target, epub.ncx.NavTarget)
        self.assertEqual(nav_target.identifier, 'part1_target-fragment')
        self.assertEqual(nav_target.value, '5')
        self.assertEqual(nav_target.class_name, 'some_class')
        self.assertEqual(nav_target.play_order, '5')
        self.assertEqual(nav_target.labels, [('Label de la Target', '', ''),])
        self.assertEqual(nav_target.src, 'Text/part1.xhtml#target-fragment')

        xml_string = """
        <navTarget>
            <navLabel xml:lang="fr"><text>Label français</text></navLabel>
            <navLabel xml:lang="en"><text>English label</text></navLabel>
            <content src="Text/part1.xhtml#target-fragment" />
        </navTarget>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_target = epub.ncx._parse_xml_nav_target(xml_element)
        self.assertEqual(nav_target.labels, [('Label français', 'fr', ''),
                                             ('English label', 'en', ''), ])

    def test_parse_xml_nav_list(self):
        """Test function "_parse_xml_nav_list"."""

        xml_string = """
        <navList id="navlist-1" class="list_class">
            <navLabel xml:lang="fr"><text>Label français</text></navLabel>
            <navLabel xml:lang="en"><text>English label</text></navLabel>
            <navInfo xml:lang="fr"><text>Info de navigation</text></navInfo>
            <navInfo xml:lang="en"><text>Navigation's info</text></navInfo>
            <navTarget playOrder="1"
                   id="part1_target-fragment"
                   value="Some Value"
                   class="some_class">
                <navLabel><text>Label de la Target 1</text></navLabel>
                <content src="Text/part1.xhtml#target-fragment" />
            </navTarget>
            <navTarget playOrder="2"
                       id="part2_target-fragment"
                       value="Some Value"
                       class="some_class">
                <navLabel><text>Label de la Target 2</text></navLabel>
                <content src="Text/part2.xhtml" />
            </navTarget>
        </navList>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_list = epub.ncx._parse_xml_nav_list(xml_element)
        self.assertIsInstance(nav_list, epub.ncx.NavList)
        self.assertEqual(nav_list.identifier, 'navlist-1')
        self.assertEqual(nav_list.class_name, 'list_class')
        self.assertEqual(nav_list.labels, [('Label français', 'fr', ''),
                                           ('English label', 'en', ''), ])
        self.assertEqual(nav_list.infos, [('Info de navigation', 'fr', ''),
                                          ('Navigation\'s info', 'en', ''), ])
        self.assertEqual(len(nav_list.nav_target), 2)

        for nav_target in nav_list.nav_target:
            self.assertIsInstance(nav_target, epub.ncx.NavTarget)
            test_label = 'Label de la Target %s' % nav_target.play_order
            self.assertEqual(nav_target.labels[0], (test_label, '', ''))

    def test_parse_xml_page_target(self):
        """Test function "_parse_xml_page_target"."""

        xml_string = """
        <pageTarget playOrder="5"
                   id="part1_target-fragment"
                   value="Some Value"
                   type="page_type"
                   class="some_class">
            <navLabel><text>Label de la Target</text></navLabel>
            <content src="Text/part1.xhtml#target-fragment" />
        </pageTarget>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        page_target = epub.ncx._parse_xml_page_target(xml_element)
        self.assertIsInstance(page_target, epub.ncx.PageTarget)
        self.assertEqual(page_target.identifier, 'part1_target-fragment')
        self.assertEqual(page_target.value, 'Some Value')
        self.assertEqual(page_target.target_type, 'page_type')
        self.assertEqual(page_target.class_name, 'some_class')
        self.assertEqual(page_target.play_order, '5')
        self.assertEqual(page_target.labels,
                         [('Label de la Target', '', ''), ])
        self.assertEqual(page_target.src, 'Text/part1.xhtml#target-fragment')

        xml_string = """
        <pageTarget>
            <navLabel xml:lang="fr"><text>Label français</text></navLabel>
            <navLabel xml:lang="en"><text>English label</text></navLabel>
            <content src="Text/part1.xhtml#target-fragment" />
        </pageTarget>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_target = epub.ncx._parse_xml_page_target(xml_element)
        self.assertEqual(nav_target.labels, [('Label français', 'fr', ''),
                                             ('English label', 'en', ''), ])

    def test_parse_xml_page_list(self):
        """Test function "_parse_xml_page_list"."""

        xml_string = """
        <pageList id="pagelist-1"
                 class="page_class">
            <navLabel xml:lang="fr"><text>Label français</text></navLabel>
            <navLabel xml:lang="en"><text>English label</text></navLabel>
            <navInfo xml:lang="fr"><text>Info de navigation</text></navInfo>
            <navInfo xml:lang="en"><text>Navigation's info</text></navInfo>
            <pageTarget playOrder="1"
                       id="part1_target-fragment"
                       value="Some Value"
                       type="page_type"
                       class="some_class">
                <navLabel xml:lang="fr"><text>Label français 1</text></navLabel>
                <content src="Text/part1.xhtml#target-fragment" />
            </pageTarget>
            <pageTarget playOrder="2"
                       id="part1_target-fragment"
                       value="Some Value"
                       type="page_type"
                       class="some_class">
                <navLabel xml:lang="fr"><text>Label français 2</text></navLabel>
                <content src="Text/part2.xhtml#target-fragment" />
            </pageTarget>
        </pageList>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        page_list = epub.ncx._parse_xml_page_list(xml_element)
        self.assertIsInstance(page_list, epub.ncx.PageList)
        self.assertEqual(page_list.identifier, 'pagelist-1')
        self.assertEqual(page_list.class_name, 'page_class')
        self.assertEqual(page_list.labels, [('Label français', 'fr', ''),
                                            ('English label', 'en', ''), ])
        self.assertEqual(page_list.infos, [('Info de navigation', 'fr', ''),
                                           ('Navigation\'s info', 'en', ''), ])
        self.assertEqual(len(page_list.page_target), 2)

        for page_target in page_list.page_target:
            self.assertIsInstance(page_target, epub.ncx.PageTarget)
            test_label = 'Label français %s' % page_target.play_order
            self.assertEqual(page_target.labels,
                             [(test_label, 'fr', ''),])

    def test_parse_xml_nav_point(self):
        """Test function "_parse_xml_nav_point"."""

        xml_string = """
        <navPoint playOrder="5"
                   id="point5"
                   class="some_class">
            <navLabel xml:lang="fr"><text>Label fr</text></navLabel>
            <navLabel xml:lang="en"><text>Label en</text></navLabel>
            <content src="Text/Point1.xhtml#fragment5" />
            <navPoint playOrder="6" id="point5_1">
                <navLabel xml:lang="fr"><text>Sous-Label 6</text></navLabel>
                <content src="Text/Point1.xhtml#fragment5_1" />
            </navPoint>
            <navPoint playOrder="7" id="point5_2">
                <navLabel xml:lang="fr"><text>Sous-Label 7</text></navLabel>
                <content src="Text/Point1.xhtml#fragment5_2" />
            </navPoint>
        </navPoint>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_point = epub.ncx._parse_xml_nav_point(xml_element)
        self.assertIsInstance(nav_point, epub.ncx.NavPoint)
        self.assertEqual(nav_point.identifier, 'point5')
        self.assertEqual(nav_point.class_name, 'some_class')
        self.assertEqual(nav_point.labels, [('Label fr', 'fr', ''),
                                             ('Label en', 'en', ''),])
        self.assertEqual(nav_point.src, 'Text/Point1.xhtml#fragment5')
        self.assertEqual(len(nav_point.nav_point), 2)
        for child_nav_point in nav_point.nav_point:
            self.assertIsInstance(child_nav_point, epub.ncx.NavPoint)
            test_label = 'Sous-Label %s' % child_nav_point.play_order
            self.assertEqual(child_nav_point.labels,
                             [(test_label, 'fr', ''),])

    def test_parse_xml_nav_map(self):
        xml_string = """
        <navMap id="the_only_one_map">
            <navPoint playOrder="1">
                <navLabel><text>Introduction</text></navLabel>
                <content src="Text/introduction.xhtml" />
            </navPoint>
            <navPoint playOrder="5"
                       id="point5"
                       class="some_class">
                <navLabel xml:lang="fr"><text>Label fr</text></navLabel>
                <navLabel xml:lang="en"><text>Label en</text></navLabel>
                <content src="Text/Point1.xhtml#fragment5" />
                <navPoint playOrder="6" id="point5_1">
                    <navLabel xml:lang="fr"><text>Sous-Label 6</text></navLabel>
                    <content src="Text/Point1.xhtml#fragment5_1" />
                </navPoint>
                <navPoint playOrder="7" id="point5_2">
                    <navLabel xml:lang="fr"><text>Sous-Label 7</text></navLabel>
                    <content src="Text/Point1.xhtml#fragment5_2" />
                </navPoint>
            </navPoint>
        </navMap>
        """
        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_map = epub.ncx._parse_xml_nav_map(xml_element)
        self.assertIsInstance(nav_map, epub.ncx.NavMap)
        self.assertEqual(nav_map.identifier, 'the_only_one_map')
        self.assertEqual(len(nav_map.nav_point), 2)
        self.assertEqual(len(nav_map.nav_point[0].nav_point), 0)
        self.assertEqual(len(nav_map.nav_point[1].nav_point), 2)

    def test_create_xml_element_text(self):
        xml_string = """<text>Some text</text>"""
        xml_element = epub.ncx._create_xml_element_text('Some text')
        self.assertEqual(xml_element.toxml(), xml_string)
        
        xml_string = """<otherText>Some text</otherText>"""
        xml_element = epub.ncx._create_xml_element_text('Some text', 'otherText')
        self.assertEqual(xml_element.toxml(), xml_string)

        xml_string = """<emptyText/>"""
        xml_element = epub.ncx._create_xml_element_text(None, 'emptyText')
        self.assertEqual(xml_element.toxml(), xml_string)

        xml_string = """<emptyText/>"""
        xml_element = epub.ncx._create_xml_element_text('', 'emptyText')
        self.assertEqual(xml_element.toxml(), xml_string)


class TestNavPoint(unittest.TestCase):
    
    def test_as_xml_element(self):
        xml_string = """<navPoint class="some_class" id="point5" playOrder="5">""" + \
            """<navLabel xml:lang="fr" dir="ltr"><text>Label fr</text></navLabel>""" + \
            """<navLabel xml:lang="en" dir="ltr"><text>Label en</text></navLabel>""" + \
            """<content src="Text/Point1.xhtml#fragment5"/>""" + \
            """<navPoint id="point5_1" playOrder="6">""" + \
                """<navLabel xml:lang="fr"><text>Sous-Label 6</text></navLabel>""" + \
                """<content src="Text/Point1.xhtml#fragment5_1"/>""" + \
            """</navPoint>""" + \
            """<navPoint id="point5_2" playOrder="7">""" + \
                """<navLabel xml:lang="fr"><text>Sous-Label 7</text></navLabel>""" + \
                """<content src="Text/Point1.xhtml#fragment5_2"/>""" + \
            """</navPoint>""" + \
        """</navPoint>"""

        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_point = epub.ncx._parse_xml_nav_point(xml_element)

        self.assertEqual(nav_point.as_xml_element().toxml(),
                         xml_element.toxml())


class TestNavMap(unittest.TestCase):
    
    def test_as_xml_element(self):
        xml_string = """<navMap id="someId">""" + \
            """<navLabel xml:lang="fr" dir="ltr"><text>Label fr</text></navLabel>""" + \
            """<navLabel xml:lang="en" dir="ltr"><text>Label en</text></navLabel>""" + \
            """<navInfo xml:lang="fr" dir="ltr"><text>Label fr</text></navInfo>""" + \
            """<navInfo xml:lang="en" dir="ltr"><text>Label en</text></navInfo>""" + \
            """<navPoint id="point5_2" playOrder="7">""" + \
                """<navLabel xml:lang="fr"><text>Sous-Label 7</text></navLabel>""" + \
                """<content src="Text/Point1.xhtml#fragment5_2"/>""" + \
            """</navPoint>""" + \
        """</navMap>"""

        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_map = epub.ncx._parse_xml_nav_map(xml_element)

        self.assertEqual(nav_map.as_xml_element().toxml(),
                         xml_element.toxml())


class TestPageTarget(unittest.TestCase):

    def test_as_xml_element(self):
        xml_string = """<pageTarget class="some_class" id="testid" playOrder="5" type="page_type" value="Some Value">""" + \
            """<navLabel xml:lang="fr" dir="ltr"><text>Label fr</text></navLabel>""" + \
            """<navLabel xml:lang="en" dir="ltr"><text>Label en</text></navLabel>""" + \
            """<content src="Text/Point1.xhtml#fragment5_2"/>""" + \
        """</pageTarget>"""

        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        page_target = epub.ncx._parse_xml_page_target(xml_element)

        self.assertEqual(page_target.as_xml_element().toxml(),
                         xml_element.toxml())


class TestPageList(unittest.TestCase):

    def test_as_xml_element(self):
        xml_string = """<pageList id="pagelist-1" class="page_class">""" + \
            """<navLabel xml:lang="fr" dir="ltr"><text>Label fr</text></navLabel>""" + \
            """<navLabel xml:lang="en" dir="ltr"><text>Label en</text></navLabel>""" + \
            """<navInfo xml:lang="fr" dir="ltr"><text>Info de navigation</text></navInfo>""" + \
            """<navInfo xml:lang="en" dir="ltr"><text>Navigation's info</text></navInfo>""" + \
            """<pageTarget class="some_class" id="testid" playOrder="5" type="page_type" value="Some Value">""" + \
                """<navLabel xml:lang="fr"><text>Label fr</text></navLabel>""" + \
                """<navLabel xml:lang="en"><text>Label en</text></navLabel>""" + \
                """<content src="Text/Point1.xhtml#fragment5_2"/>""" + \
            """</pageTarget>""" + \
        """</pageList>"""

        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        page_list = epub.ncx._parse_xml_page_list(xml_element)

        self.assertEqual(page_list.as_xml_element().toxml(),
                         xml_element.toxml())


class TestNavTarget(unittest.TestCase):

    def test_as_xml_element(self):
        xml_string = """<navTarget class="some_class" id="testid" playOrder="5" value="5">""" + \
            """<navLabel xml:lang="fr" dir="ltr"><text>Label fr</text></navLabel>""" + \
            """<navLabel xml:lang="en" dir="ltr"><text>Label en</text></navLabel>""" + \
            """<content src="Text/Point1.xhtml#fragment5_2"/>""" + \
        """</navTarget>"""

        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_target = epub.ncx._parse_xml_nav_target(xml_element)

        self.assertEqual(nav_target.as_xml_element().toxml(),
                         xml_element.toxml())


class TestNavList(unittest.TestCase):

    def test_as_xml_element(self):
        xml_string = """<navList class="some_class" id="testid">""" + \
            """<navLabel xml:lang="fr" dir="ltr"><text>Label fr</text></navLabel>""" + \
            """<navLabel xml:lang="en" dir="ltr"><text>Label en</text></navLabel>""" + \
            """<navInfo xml:lang="fr" dir="ltr"><text>Info de navigation</text></navInfo>""" + \
            """<navInfo xml:lang="en" dir="ltr"><text>Navigation's info</text></navInfo>""" + \
            """<navTarget class="some_class" id="testid" playOrder="5" value="5">""" + \
                """<navLabel xml:lang="fr"><text>Label fr</text></navLabel>""" + \
                """<navLabel xml:lang="en"><text>Label en</text></navLabel>""" + \
                """<content src="Text/Point1.xhtml#fragment5_2"/>""" + \
            """</navTarget>""" + \
        """</navList>"""

        xml_element = minidom.parseString(xml_string.encode('utf-8')).documentElement
        nav_list = epub.ncx._parse_xml_nav_list(xml_element)

        self.assertEqual(nav_list.as_xml_element().toxml(),
                         xml_element.toxml())


class TestNcx(unittest.TestCase):
    
    def test_as_xml_document(self):
        """Check if ncx.as_xml_document reproduce a good xml.
        
        ... And yeah, I hate XML with unit testing :("""
        
        xml_string = """<?xml version="1.0" ?>
<ncx version="2005-1" xml:lang="en-US" xmlns="http://www.daisy.org/z3986/2005/ncx/">
    <head>
        <meta content="org-example-5059463624137734586" name="dtb:uid"/>
        <meta content="2" name="dtb:depth"/>
        <meta content="3907" name="dtb:totalPageCount"/>
        <meta content="7814" name="dtb:maxPageNumber"/>
        <meta content="Epub Test" name="dtb:generator"/>
    </head>
    <docTitle>
        <text>Selections from &quot;Great Pictures, As Seen and Described by Famous Writers&quot;</text>
    </docTitle>
    <docAuthor>
        <text>Esther Singleton</text>
    </docAuthor>
    <docAuthor>
        <text>Test Author</text>
    </docAuthor>
    <navMap>
        <navPoint class="h1" id="ch1">
            <navLabel>
                <text>Chapter 1</text>
            </navLabel>
            <content src="content.html#ch_1"/>
            <navPoint class="h2" id="ch_1_1">
                <navLabel>
                    <text>Chapter 1.1</text>
                </navLabel>
                <content src="content.html#ch_1_1"/>
            </navPoint>
        </navPoint>
        <navPoint class="h1" id="ncx-2">
            <navLabel>
                <text>Chapter 2</text>
            </navLabel>
            <content src="content.html#ch_2"/>
        </navPoint>
    </navMap>
    <pageList>
        <pageTarget id="p1" type="normal" value="1">
            <navLabel dir="ltr">
                <text>1</text>
            </navLabel>
            <content src="content.html#p1"/>
        </pageTarget>
        <pageTarget id="p2" type="normal" value="2">
            <navLabel>
                <text>2</text>
            </navLabel>
            <content src="content.html#p2"/>
        </pageTarget>
    </pageList>
    <navList>
        <navLabel>
            <text>List of Illustrations</text>
        </navLabel>
        <navTarget id="ill-1">
            <navLabel>
                <text>Portratit of Georg Gisze (Holbein)</text>
            </navLabel>
            <content src="content.html#ill1"/>
        </navTarget>
        <navTarget id="ill-2">
            <navLabel>
                <text>The adoration of the lamb (Van Eyck)</text>
            </navLabel>
            <content src="content.html#ill2"/>
        </navTarget>
    </navList>
</ncx>
"""

        self.maxDiff = None

        toc = epub.ncx.parse_toc(xml_string)
        xml_toc = toc.as_xml_document().toprettyxml('    ')

        xml_input = xml_string.strip()
        xml_output = xml_toc.strip()

        self.assertEqual(xml_output, xml_input)
