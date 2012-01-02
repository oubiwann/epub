# -*- coding: utf-8 -*-

"""
Module de lecture des fichiers NCX pour epub.

NCX doc: http://www.niso.org/workrooms/daisy/Z39-86-2005.html#NCX
NCX Epub spec: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4.1
"""

from xml.dom import minidom

MIMETYPE = u'application/x-dtbncx+xml'

def parse_toc(xmlstring):
    """Parse un document xml NCX à partir d'une chaîne de caractères."""
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

    # Get title (<docTitle> tag is required)
    toc.title = _parse_for_text_tag(toc_xml.getElementsByTagName('docTitle')[0])

    # Get authors (<docAuthor> tags are optionnal)
    for author in toc_xml.getElementsByTagName('docAuthor'):
        toc.authors.append(_parse_for_text_tag(author))

    # Inspect <navMap>
    toc.nav_map = _parse_xml_nav_map(toc_xml.getElementsByTagName('navMap')[0])

    # Inspect <pageList> (if exist)
    for page_list in toc_xml.getElementsByTagName('pageList'):
        for page_target in page_list.getElementsByTagName('pageTarget'):
            toc.page_list.append(_parse_xml_page_target(page_target))

    return toc

def _parse_xml_nav_map(element):
    """Parse un ELEMENT_NODE <navMap> et retourne un objet NcxNavMap"""
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
    """Parse un ELEMENT_NODE <navPoint> et retourne un objet NcxNavPoint"""
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
    """Parse un ELEMENT_NODE <pageList> et retourne un objet NcxPageList"""
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
        elif node.tagName == 'navPoint':
            page_list.add_target(_parse_xml_page_target(node))

def _parse_xml_page_target(element):
    """Parse un ELEMENT_NODE <pageTarget> et retourne un objet NcxPageTarget"""
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

def _parse_for_text_tag(xml_element, name=u'text'):
    """Parse un ELEMENT_NODE pour obtenir le texte de son enfant
    
    Les fichiers ncx contiennent souvent "navLabel" > "text" > TEXT_NODE, et 
    cette fonction permet ainsi de factoriser les nombreux traitements.
    
    Le second paramètre permet de fournir un nom au tag fils recherché ("text" 
    par défaut).
    
    Cette fonction retourne une chaine vide si rien n'est trouvé, sans lever 
    d'erreur.
    """
    tags = xml_element.getElementsByTagName(name)
    text = u''
    if len(tags) > 0:
        tag = tags[0]
        tag.normalize()
        text = tag.firstChild.data
    return text


class NcxFile(object):
    """Représente le contenu structuré d'un fichier NCX."""

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
        self.nav_map = NcxNavMap()
        self.page_list = []
        self.nav_lists = []


class NcxNavMap(object):
    """Représente la navMap d'un fichier NCX"""

    id = None
    labels = None
    infos = None
    map = None

    def __init__(self):
        self.id = None
        self.labels = []
        self.infos = []
        self.map = []

    def add_label(self, label, lang=u'', dir=u''):
        self.labels.append((label, lang, dir))

    def add_info(self, label, lang=u'', dir=u''):
        self.infos.append((label, lang, dir))

    def add_point(self, point):
        self.map.append(point)


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
