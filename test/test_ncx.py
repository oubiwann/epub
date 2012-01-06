# -*- coding: utf-8 -*-

import unittest

from xml.dom import minidom

from epub import ncx

class TestParseFunction(unittest.TestCase):
    """Test case for all the _parse_* function."""

    def test_parse_for_text_tag(self):
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
        self.assertEqual(text, u'')

    def test_parse_xml_nav_target(self):
        pass

    def test_parse_xml_nav_list(self):
        pass

    def test_parse_xml_page_target(self):
        pass

    def test_parse_xml_page_list(self):
        pass

    def test_parse_xml_nav_point(self):
        pass

    def test_parse_xml_nav_map(self):
        pass
