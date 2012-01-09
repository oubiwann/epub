# -*- coding: utf-8 -*-

"""
Python lib for reading NCX formated file for epub.

There is some difference between NCX original format and one for Epub; see 
officiel documention for more information.1111

NCX doc: http://www.niso.org/workrooms/daisy/Z39-86-2005.html#NCX
NCX Epub spec: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4.1
"""

from xml.dom import minidom

def parse_toc(xmlstring):
    """Inspect an NCX formated xml document."""
    toc = NcxFile()
    toc_xml = minidom.parseString(xmlstring).documentElement

    # Inspect head > meta; unknow meta are ignored
    head = toc_xml.getElementsByTagName(u'head')[0]
    metas = {'dtb:uid': u'',
             'dtb:depth': u'',
             'dtb:totalPageCount': u'',
             'dtb:maxPageNumber': u'',
             'dtb:generator': u''}

    for meta in head.getElementsByTagName('meta'):
        metas[meta.getAttribute('name')] = meta.getAttribute('content')

    toc.uid = metas['dtb:uid']
    toc.depth = metas['dtb:depth']
    toc.total_page_count = metas['dtb:totalPageCount']
    toc.max_page_number = metas['dtb:maxPageNumber']
    toc.generator = metas['dtb:generator']

    # Get title (one and only one <docTitle> tag is required)
    toc.title = _parse_for_text_tag(toc_xml.getElementsByTagName('docTitle')[0])

    # Get authors (<docAuthor> tags are optionnal)
    for author in toc_xml.getElementsByTagName('docAuthor'):
        toc.authors.append(_parse_for_text_tag(author))

    # Inspect <navMap> (one is required)
    toc.nav_map = _parse_xml_nav_map(toc_xml.getElementsByTagName('navMap')[0])

    # Inspect <pageList> (optionnal, only one)
    page_lists = toc_xml.getElementsByTagName('pageList')
    if len(page_lists) > 0:
        toc.page_list = _parse_xml_page_list(page_lists[0])

    # Inspect <navList> (optionnal, many are possible)
    for nav_list in toc_xml.getElementsByTagName('navList'):
        toc.add_nav_list(_parse_xml_nav_list(nav_list))

    return toc

def _parse_xml_nav_map(element):
    """Inspect an xml.dom.Element <navMap> and return a NcxNavMap object."""
    nav_map = NcxNavMap()
    nav_map.id = element.getAttribute('id')

    children = [e for e in element.childNodes if e.nodeType == e.ELEMENT_NODE]
    for node in children:
        if node.tagName == 'navLabel':
            nav_map.add_label(_parse_for_text_tag(node),
                              node.getAttribute('xml:lang'),
                              node.getAttribute('dir'))
        elif node.tagName == 'navInfo':
            nav_map.add_info(_parse_for_text_tag(node),
                             node.getAttribute('xml:lang'),
                             node.getAttribute('dir'))
        elif node.tagName == 'navPoint':
            nav_map.add_point(_parse_xml_nav_point(node))

    return nav_map

def _parse_xml_nav_point(element):
    """Inspect an xml.dom.Element <navPoint> and return a NcxNavPoint object."""
    nav_point = NcxNavPoint()
    nav_point.id = element.getAttribute('id')
    nav_point.class_name = element.getAttribute('class')
    nav_point.play_order = element.getAttribute('playOrder')

    children = [e for e in element.childNodes if e.nodeType == e.ELEMENT_NODE]
    for node in children:
        if node.tagName == 'navLabel':
            nav_point.add_label(_parse_for_text_tag(node),
                                node.getAttribute('xml:lang'),
                                node.getAttribute('dir'))
        elif node.tagName == 'content':
            nav_point.src = node.getAttribute('src')
        elif node.tagName == 'navPoint':
            nav_point.add_point(_parse_xml_nav_point(node))

    return nav_point

def _parse_xml_page_list(element):
    """Inspect an xml.dom.Element <pageList> and return a NcxPageList object."""
    page_list = NcxPageList()
    page_list.id = element.getAttribute('id')
    page_list.class_name = element.getAttribute('class')

    children = [e for e in element.childNodes if e.nodeType == e.ELEMENT_NODE]
    for node in children:
        if node.tagName == 'navLabel':
            page_list.add_label(_parse_for_text_tag(node),
                                node.getAttribute('xml:lang'),
                                node.getAttribute('dir'))
        elif node.tagName == 'navInfo':
            page_list.add_info(_parse_for_text_tag(node),
                               node.getAttribute('xml:lang'),
                               node.getAttribute('dir'))
        elif node.tagName == 'pageTarget':
            page_list.add_target(_parse_xml_page_target(node))

    return page_list

def _parse_xml_page_target(element):
    """Inspect an xml.dom.Element <pageTarget> and return a NcxPageTarget object."""
    page_target = NcxPageTarget()
    page_target.id = element.getAttribute('id')
    page_target.value = element.getAttribute('value')
    page_target.type = element.getAttribute('type')
    page_target.class_name = element.getAttribute('class')
    page_target.play_order = element.getAttribute('playOrder')

    children = [e for e in element.childNodes if e.nodeType == e.ELEMENT_NODE]
    for node in children:
        if node.tagName == 'navLabel':
            page_target.add_label(_parse_for_text_tag(node),
                                  node.getAttribute('xml:lang'),
                                  node.getAttribute('dir'))
        elif node.tagName == 'content':
            page_target.src = node.getAttribute('src')

    return page_target

def _parse_xml_nav_list(element):
    """Inspect an xml.dom.Element <navList> and return a NcxNavList object."""
    nav_list = NcxNavList()
    nav_list.id = element.getAttribute('id')
    nav_list.class_name = element.getAttribute('class')

    children = [e for e in element.childNodes if e.nodeType == e.ELEMENT_NODE]
    for node in children:
        if node.tagName == 'navLabel':
            nav_list.add_label(_parse_for_text_tag(node),
                                node.getAttribute('xml:lang'),
                                node.getAttribute('dir'))
        elif node.tagName == 'navInfo':
            nav_list.add_info(_parse_for_text_tag(node),
                               node.getAttribute('xml:lang'),
                               node.getAttribute('dir'))
        elif node.tagName == 'navTarget':
            nav_list.add_target(_parse_xml_nav_target(node))

    return nav_list

def _parse_xml_nav_target(element):
    """Inspect an xml.dom.Element <navTarget> and return a NcxNavTarget 
    object."""
    nav_target = NcxNavTarget()
    nav_target.id = element.getAttribute('id')
    nav_target.value = element.getAttribute('value')
    nav_target.class_name = element.getAttribute('class')
    nav_target.play_order = element.getAttribute('playOrder')

    children = [e for e in element.childNodes if e.nodeType == e.ELEMENT_NODE]
    for node in children:
        if node.tagName == 'navLabel':
            nav_target.add_label(_parse_for_text_tag(node),
                                  node.getAttribute('xml:lang'),
                                  node.getAttribute('dir'))
        elif node.tagName == 'content':
            nav_target.src = node.getAttribute('src')

    return nav_target

def _parse_for_text_tag(xml_element, name=u'text'):
    """Inspect an xml.dom.Element with a child 'name' to get its text value.
    
    NCX file has many element with a child likes "navLabel" > "text" > TEXT_NODE
    and this function allow to avoid some boilerplate code.
    
    First parameter must be an xml.dom.Element, having one child named by the 
    second parameter (by default a "text" tag).
    
    If nothing is founded, an empty string u'' is returned.
    """

    tags = xml_element.getElementsByTagName(name)
    text = u''
    if len(tags) > 0:
        tag = tags[0]
        tag.normalize()
        text = tag.firstChild.data
    return text


class NcxFile(object):
    """Represent the structured content of a NCX file."""

    uid = None
    depth = None
    total_page_count = None
    max_page_number = None
    generator = None 
    title = None
    authors = None
    nav_map = None
    page_list = None
    nav_lists = None

    def __init__(self):
        self.uid = None
        self.depth = None
        self.total_page_count = None
        self.max_page_number = None
        self.generator = None 
        self.title = None
        self.authors = []
        self.nav_map = None
        self.page_list = None
        self.nav_lists = []

    def add_nav_list(self, nav_list):
        self.nav_lists.append(nav_list)

class NcxNavMap(object):
    """Represente navMap tag of an NCX file."""

    id = None
    labels = None
    infos = None
    nav_point = None

    def __init__(self):
        self.id = None
        self.labels = []
        self.infos = []
        self.nav_point = []

    def add_label(self, label, lang=u'', dir=u''):
        self.labels.append((label, lang, dir))

    def add_info(self, label, lang=u'', dir=u''):
        self.infos.append((label, lang, dir))

    def add_point(self, point):
        self.nav_point.append(point)


class NcxNavPoint(object):
    id = None
    class_name = None
    play_order = None
    labels = None
    src = None
    nav_point = None

    def __init__(self):
        self.id = None
        self.class_name = None
        self.play_order = None
        self.labels = []
        self.src = None
        self.nav_point = []

    def add_label(self, label, lang=u'', dir=u''):
        self.labels.append((label, lang, dir))

    def add_point(self, nav_point):
        self.nav_point.append(nav_point)

class NcxPageList(object):
    id = None
    class_name = None
    labels = None
    infos = None
    page_target = None

    def __init__(self):
        self.id = None
        self.class_nampe = None
        self.page_target = []
        self.labels = []
        self.infos = []

    def add_label(self, label, lang=u'', dir=u''):
        self.labels.append((label, lang, dir))

    def add_info(self, label, lang=u'', dir=u''):
        self.infos.append((label, lang, dir))

    def add_target(self, page_target):
        self.page_target.append(page_target)

class NcxPageTarget(object):
    id = None
    value = None
    type = None
    class_name = None
    play_order = None
    src = None
    labels = None

    def __init__(self):
        self.id = None
        self.value = None
        self.type = None
        self.class_name = None
        self.play_order = None
        self.src = None
        self.labels = []

    def add_label(self, label, lang=u'', dir=u''):
        self.labels.append((label, lang, dir))

class NcxNavList(object):
    id = None
    class_name = None
    labels = None
    infos = None
    nav_target = None

    def __init__(self):
        self.id = None
        self.class_nampe = None
        self.nav_target = []
        self.labels = []
        self.infos = []

    def add_label(self, label, lang=u'', dir=u''):
        self.labels.append((label, lang, dir))

    def add_info(self, label, lang=u'', dir=u''):
        self.infos.append((label, lang, dir))

    def add_target(self, nav_target):
        self.nav_target.append(nav_target)

class NcxNavTarget(object):
    id = None
    class_name = None
    play_order = None
    labels = None
    src = None

    def __init__(self):
        self.id = None
        self.class_name = None
        self.play_order = None
        self.labels = []
        self.src = None

    def add_label(self, label, lang=u'', dir=u''):
        self.labels.append((label, lang, dir))

