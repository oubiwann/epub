# -*- coding: utf-8 -*-

import unittest

from xml.dom import minidom

from epub import ncx

class TestParseFunction(unittest.TestCase):
    """Test case for all the _parse_* function."""

    def test_parse_for_text_tag(self):
        """Test function "_parse_for_text_tag"."""

        xml_string = """
        <someTag>
            <text>La balise "text" par défaut.</text>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        text = ncx._parse_for_text_tag(xml_element)
        self.assertEqual(text, u'La balise "text" par défaut.')

        xml_string = """
        <someTag>
            <otherTag>La balise "otherTag" par le paramètre "name".</otherTag>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        text = ncx._parse_for_text_tag(xml_element, 'otherTag')
        self.assertEqual(text, u'La balise "otherTag" par le paramètre "name".')

        xml_string = """
        <someTag>
            <text>Mauvaise balise !</text>
            <textOk>Bonne balise !</textOk>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        text = ncx._parse_for_text_tag(xml_element, 'textOk')
        self.assertEqual(text, u'Bonne balise !')

        xml_string = """
        <someTag>
            <text>Première balise uniquement...</text>
            <text>Pas la seconde !</text>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        text = ncx._parse_for_text_tag(xml_element)
        self.assertEqual(text, u'Première balise uniquement...')
        
        xml_string = """
        <someTag>
            <text>Je ne cherche pas "text" !</text>
        </someTag>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        text = ncx._parse_for_text_tag(xml_element, 'noText')
        self.assertEqual(text, u'', u'Il ne devrait pas y avoir de résultat !')

    def test_parse_xml_nav_target(self):
        """Test function "_parse_xml_nav_target"."""
        
        xml_string = """
        <navTarget playOrder="5"
                   id="part1_target-fragment"
                   value="Some Value"
                   class="some_class">
            <navLabel><text>Label de la Target</text></navLabel>
            <content src="Text/part1.xhtml#target-fragment" />
        </navTarget>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        nav_target = ncx._parse_xml_nav_target(xml_element)
        self.assertIsInstance(nav_target, ncx.NcxNavTarget)
        self.assertEqual(nav_target.id, u'part1_target-fragment')
        self.assertEqual(nav_target.value, u'Some Value')
        self.assertEqual(nav_target.class_name, u'some_class')
        self.assertEqual(nav_target.play_order, u'5')
        self.assertEqual(nav_target.labels, [(u'Label de la Target', '', ''),])
        self.assertEqual(nav_target.src, u'Text/part1.xhtml#target-fragment')
        
        xml_string = """
        <navTarget>
            <navLabel xml:lang="fr"><text>Label français</text></navLabel>
            <navLabel xml:lang="en"><text>English label</text></navLabel>
            <content src="Text/part1.xhtml#target-fragment" />
        </navTarget>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        nav_target = ncx._parse_xml_nav_target(xml_element)
        self.assertEqual(nav_target.labels, [(u'Label français', 'fr', ''),
                                             (u'English label', 'en', ''),])

    def test_parse_xml_nav_list(self):
        """Test function "_parse_xml_nav_list"."""
        
        xml_string = """
        <navList id="navlist-1"
                 class="list_class">
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
        xml_element = minidom.parseString(xml_string).documentElement
        nav_list = ncx._parse_xml_nav_list(xml_element)
        self.assertIsInstance(nav_list, ncx.NcxNavList)
        self.assertEqual(nav_list.id, u'navlist-1')
        self.assertEqual(nav_list.class_name, u'list_class')
        self.assertEqual(nav_list.labels, [(u'Label français', 'fr', ''),
                                             (u'English label', 'en', ''),])
        self.assertEqual(nav_list.infos, [(u'Info de navigation', 'fr', ''),
                                             (u'Navigation\'s info', 'en', ''),])
        self.assertEqual(len(nav_list.nav_target), 2)

        for nav_target in nav_list.nav_target:
            self.assertIsInstance(nav_target, ncx.NcxNavTarget)
            test_label = u'Label de la Target %s' % nav_target.play_order
            self.assertEqual(nav_target.labels[0],
                             (test_label, u'', u''))

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
        xml_element = minidom.parseString(xml_string).documentElement
        page_target = ncx._parse_xml_page_target(xml_element)
        self.assertIsInstance(page_target, ncx.NcxPageTarget)
        self.assertEqual(page_target.id, u'part1_target-fragment')
        self.assertEqual(page_target.value, u'Some Value')
        self.assertEqual(page_target.type, u'page_type')
        self.assertEqual(page_target.class_name, u'some_class')
        self.assertEqual(page_target.play_order, u'5')
        self.assertEqual(page_target.labels, [(u'Label de la Target', '', ''),])
        self.assertEqual(page_target.src, u'Text/part1.xhtml#target-fragment')
        
        xml_string = """
        <pageTarget>
            <navLabel xml:lang="fr"><text>Label français</text></navLabel>
            <navLabel xml:lang="en"><text>English label</text></navLabel>
            <content src="Text/part1.xhtml#target-fragment" />
        </pageTarget>
        """
        xml_element = minidom.parseString(xml_string).documentElement
        nav_target = ncx._parse_xml_page_target(xml_element)
        self.assertEqual(nav_target.labels, [(u'Label français', 'fr', ''),
                                             (u'English label', 'en', ''),])

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
        xml_element = minidom.parseString(xml_string).documentElement
        page_list = ncx._parse_xml_page_list(xml_element)
        self.assertIsInstance(page_list, ncx.NcxPageList)
        self.assertEqual(page_list.id, u'pagelist-1')
        self.assertEqual(page_list.class_name, u'page_class')
        self.assertEqual(page_list.labels, [(u'Label français', 'fr', ''),
                                             (u'English label', 'en', ''),])
        self.assertEqual(page_list.infos, [(u'Info de navigation', 'fr', ''),
                                             (u'Navigation\'s info', 'en', ''),])
        self.assertEqual(len(page_list.page_target), 2)

        for page_target in page_list.page_target:
            self.assertIsInstance(page_target, ncx.NcxPageTarget)
            test_label = u'Label français %s' % page_target.play_order
            self.assertEqual(page_target.labels,
                             [(test_label, u'fr', u''),])

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
        xml_element = minidom.parseString(xml_string).documentElement
        nav_point = ncx._parse_xml_nav_point(xml_element)
        self.assertIsInstance(nav_point, ncx.NcxNavPoint)
        self.assertEqual(nav_point.id, u'point5')
        self.assertEqual(nav_point.class_name, u'some_class')
        self.assertEqual(nav_point.labels, [(u'Label fr', 'fr', ''),
                                             (u'Label en', 'en', ''),])
        self.assertEqual(nav_point.src, u'Text/Point1.xhtml#fragment5')
        self.assertEqual(len(nav_point.nav_point), 2)
        for child_nav_point in nav_point.nav_point:
            self.assertIsInstance(child_nav_point, ncx.NcxNavPoint)
            test_label = u'Sous-Label %s' % child_nav_point.play_order
            self.assertEqual(child_nav_point.labels,
                             [(test_label, u'fr', u''),])

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
        xml_element = minidom.parseString(xml_string).documentElement
        nav_map = ncx._parse_xml_nav_map(xml_element)
        self.assertIsInstance(nav_map, ncx.NcxNavMap)
        self.assertEqual(nav_map.id, u'the_only_one_map')
        self.assertEqual(len(nav_map.nav_point), 2)
        self.assertEqual(len(nav_map.nav_point[0].nav_point), 0)
        self.assertEqual(len(nav_map.nav_point[1].nav_point), 2)
