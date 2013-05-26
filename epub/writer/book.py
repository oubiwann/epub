# -*- coding: utf-8 -*-

# Copyright (c) 2012, Bin Tan
# This file is distributed under the BSD Licence. See
# python-epub-builder-license.txt for details.
from cStringIO import StringIO
import itertools
import mimetypes
import os
import shutil
import subprocess
import sys
import uuid
import zipfile

import progressbar

from lxml import etree

from genshi.template import TemplateLoader

from epub import const


class ToCMapNode(object):

    def __init__(self):
        self.playOrder = 0
        self.title = ''
        self.href = ''
        self.children = []
        self.depth = 0

    def assign_playOrder(self):
        nextplayOrder = [0]
        self._assign_playOrder(nextplayOrder)

    def _assign_playOrder(self, nextplayOrder):
        self.playOrder = nextplayOrder[0]
        nextplayOrder[0] = self.playOrder + 1
        for child in self.children:
            child._assign_playOrder(nextplayOrder)


class EPubItem(object):

    def __init__(self):
        self.id = ''
        self.srcPath = ''
        self.dest_path = ''
        self.mime_type = ''
        self.html = ''


class EPubBook(object):

    def __init__(self, template_dir=None, display_progress=True):
        self.loader = TemplateLoader(template_dir)

        self.root_dir = ''
        self.uuid = uuid.uuid1()

        self.lang = 'en-US'
        self.title = ''
        self.creators = []
        self.meta_info = []

        self.image_items = {}
        self.html_items = {}
        self.css_items = {}
        self.script_items = {}

        self.cover_image = None
        self.title_page = None
        self.toc_page = None

        self.spine = []
        self.guide = {}
        self.toc_map_root = ToCMapNode()
        self.last_node_at_depth = {0 : self.toc_map_root}
        self.display_progress = display_progress

    def set_title(self, title):
        self.title = title

    def set_lang(self, lang):
        self.lang = lang

    def add_creator(self, name, role = 'aut'):
        self.creators.append((name, role))

    def add_meta(self, metaName, metaValue, **metaAttrs):
        self.meta_info.append((metaName, metaValue, metaAttrs))

    def get_meta_tags(self):
        l = []
        for metaName, metaValue, metaAttr in self.meta_info:
            beginTag = '<dc:%s' % metaName
            if metaAttr:
                for attrName, attrValue in metaAttr.iteritems():
                    beginTag += ' opf:%s="%s"' % (attrName, attrValue)
            beginTag += '>'
            endTag = '</dc:%s>' % metaName
            l.append((beginTag, metaValue, endTag))
        return l

    def get_image_items(self):
        return sorted(self.image_items.values(), key = lambda x : x.id)

    def get_html_items(self):
        return sorted(self.html_items.values(), key = lambda x : x.id)

    def get_css_items(self):
        return sorted(self.css_items.values(), key = lambda x : x.id)

    def get_script_items(self):
        return sorted(self.script_items.values(), key = lambda x : x.id)

    def get_all_items(self):
        # XXX debug
        #print '   Items in ebook:'
        #print '     HTML:', len(self.html_items)
        #print '     CSS:', len(self.css_items)
        #print '     JS:', len(self.script_items)
        #print '     Images:', len(self.image_items)
        return sorted(itertools.chain(self.image_items.values(), self.html_items.values(), self.css_items.values(), self.script_items.values()), key = lambda x : x.id)

    def add_mage(self, srcPath, dest_path):
        item = EPubItem()
        item.id = 'image_%d' % (len(self.image_items) + 1)
        item.srcPath = srcPath
        item.dest_path = dest_path
        item.mime_type = mimetypes.guess_type(dest_path)[0]
        #assert item.dest_path not in self.image_items
        if item.dest_path not in self.image_items:
	        #print '  + adding Image', srcPath, item.id
        	self.image_items[item.dest_path] = item
        return self.image_items[item.dest_path]

    def add_html_for_image(self, imageItem):
        tmpl = self.loader.load('image.html')
        stream = tmpl.generate(book=self, item = imageItem)
        html = stream.render('xhtml', doctype = 'xhtml11', drop_xml_decl = False)
        return self.add_html('', '%s.html' % imageItem.dest_path, html)

    def add_html(self, srcPath, dest_path, html = None):
        item = EPubItem()
        item.id = 'html_%d' % (len(self.html_items) + 1)
        item.srcPath = srcPath
        item.dest_path = dest_path
        if html is not None:
            item.html = html
        item.mime_type = const.MIMETYPE_HTML
        if item.dest_path not in self.html_items:
	        #print '  + adding Page', srcPath, item.id
        	self.html_items[item.dest_path] = item
        return self.html_items[item.dest_path]

    def add_css(self, srcPath, dest_path):
        item = EPubItem()
        item.id = 'css_%d' % (len(self.css_items) + 1)
        item.srcPath = srcPath
        item.dest_path = dest_path
        item.mime_type = const.MIMETYPE_CSS
        #assert item.dest_path not in self.css_items
        if item.dest_path not in self.css_items:
	        #print '  + adding CSS', srcPath, item.id
        	self.css_items[item.dest_path] = item
        return self.css_items[item.dest_path]

    def add_script(self, srcPath, dest_path):
        item = EPubItem()
        item.id = 'js_%d' % (len(self.script_items) + 1)
        item.srcPath = srcPath
        item.dest_path = dest_path
        item.mime_type = const.MIMETYPE_JS
        if item.dest_path not in self.script_items:
	        #print '  + adding JS', srcPath, item.id
        	self.script_items[item.dest_path] = item
        return self.script_items[item.dest_path]

    def add_cover(self, srcPath):
        assert not self.cover_image
        _, ext = os.path.splitext(srcPath)
        dest_path = 'cover%s' % ext
        self.cover_image = self.add_mage(srcPath, dest_path)
        #coverPage = self.add_html_for_image(self.cover_image)
        #self.add_spine_item(coverPage, False, -300)
        #self.add_guide_item(coverPage.dest_path, 'Cover', 'cover')

    def _make_title_page(self):
        assert self.title_page
        if self.title_page.html:
            return
        from epub.writer import book
        path = book.__file__
        # XXX debug
        #import pdb;pdb.set_trace()
        tmpl = self.loader.load('title-page.html')
        stream = tmpl.generate(book=self)
        self.title_page.html = stream.render('xhtml', doctype = 'xhtml11', drop_xml_decl = False)

    def add_title_page(self, html = ''):
        assert not self.title_page
        self.title_page = self.add_html('', 'title-page.html', html)
        self.add_spine_item(self.title_page, True, -200)
        self.add_guide_item('title-page.html', 'Title Page', 'title-page')

    def _make_toc_page(self):
        assert self.toc_page
        tmpl = self.loader.load('toc.html')
        stream = tmpl.generate(book=self)
        self.toc_page.html = stream.render(
            'xhtml', doctype='xhtml11', drop_xml_decl=False)

    def add_toc_page(self):
        assert not self.toc_page
        self.toc_page = self.add_html('', 'toc.html', '')
        self.add_spine_item(self.toc_page, False, -100)
        self.add_guide_item('toc.html', 'Table of Contents', 'toc')

    def get_spine(self):
        return sorted(self.spine)

    def add_spine_item(self, item, linear = True, order=None):
        assert item.dest_path in self.html_items
        if order == None:
            order = (max(order for order, _, _ in self.spine)
                        if self.spine else 0) + 1
        self.spine.append((order, item, linear))

    def get_guide(self):
        return sorted(self.guide.values(), key = lambda x : x[2])

    def add_guide_item(self, href, title, type):
        assert type not in self.guide
        self.guide[type] = (href, title, type)

    def get_toc_map_root(self):
        return self.toc_map_root

    def get_toc_map_height(self):
        return max(self.last_node_at_depth.keys())

    def add_toc_map_node(self, href, title, depth = None, parent = None):
        node = ToCMapNode()
        node.href = href
        node.title = title
        if parent == None:
            if depth == None:
                parent = self.toc_map_root
            else:
                parent = self.last_node_at_depth[depth - 1]
        parent.children.append(node)
        node.depth = parent.depth + 1
        self.last_node_at_depth[node.depth] = node
        return node

    def make_dirs(self):
        try:
            os.makedirs(os.path.join(self.root_dir, 'META-INF'))
        except OSError:
            pass
        try:
            os.makedirs(os.path.join(self.root_dir, 'OEBPS'))
        except OSError:
            pass

    def _write_container_xml(self):
        fout = open(os.path.join(self.root_dir, const.CONTAINER_PATH), 'w')
        tmpl = self.loader.load('container.xml')
        stream = tmpl.generate()
        fout.write(stream.render('xml'))
        fout.close()

    def _write_toc_ncx(self):
        self.toc_map_root.assign_playOrder()
        fout = open(os.path.join(self.root_dir, const.NCX_PATH), 'w')
        tmpl = self.loader.load('toc.ncx')
        stream = tmpl.generate(book=self)
        fout.write(stream.render('xml'))
        fout.close()

    def _write_content_opf(self):
        fout = open(os.path.join(self.root_dir, const.OPF_PATH), 'w')
        tmpl = self.loader.load('content.opf')
        stream = tmpl.generate(book=self)
        fout.write(stream.render('xml'))
        fout.close()

    def _write_items(self):
        items = self.get_all_items()
        if self.display_progress:
            output = sys.stderr
        else:
            output = StringIO()
        pbar = progressbar.ProgressBar(
            maxval=len(items),
        	widgets=[progressbar.Percentage(), progressbar.Counter('%5d'),
        	   progressbar.Bar(), progressbar.ETA()],
            fd=output).start()
        for item in items:
            #print item.id, item.dest_path
            outname = os.path.join(self.root_dir, 'OEBPS', item.dest_path)
            if item.html:
                # XXX debug
                #print '   writing html to %s' % (outname)
                fout = open(outname, 'w')
                fout.write(item.html)
                fout.close()
            else:
                # XXX debug
                #print '   copying %s --> %s' % (item.srcPath, outname)
                shutil.copyfile(item.srcPath, outname)
        	pbar.update(pbar.currval + 1)
        pbar.finish()

    def _write_mime_type(self):
        fout = open(os.path.join(self.root_dir, 'mime_type'), 'w')
        fout.write(const.MIMETYPE_EPUB)
        fout.close()

    @staticmethod
    def _list_manifest_items(contentOPFPath):
        tree = etree.parse(contentOPFPath)
        return tree.xpath(
            "//opf:manifest/opf:item/@href",
            namespaces={'opf': 'http://www.idpf.org/2007/opf'})

    @staticmethod
    def create_archive(root_dir, output_path):
        fout = zipfile.ZipFile(output_path, 'w')
        cwd = os.getcwd()
        os.chdir(root_dir)
        fout.write('mime_type', compress_type = zipfile.ZIP_STORED)
        fileList = []
        fileList.append(const.CONTAINER_PATH)
        fileList.append(const.OPF_PATH)
        for itemPath in EPubBook._list_manifest_items(const.OPF_PATH):
            fileList.append(os.path.join('OEBPS', itemPath))
        for filePath in fileList:
            fout.write(filePath, compress_type = zipfile.ZIP_DEFLATED)
        fout.close()
        os.chdir(cwd)

    @staticmethod
    def check_epub(checkerPath, epubPath):
        cmd = ['java', '-jar', checkerPath, epubPath]
        #print cmd
        subprocess.call(cmd, shell=False)

    def create_book(self, root_dir, extension='.epub'):
        if self.title_page:
            self._make_title_page()
        if self.toc_page:
            self._make_toc_page()
        self.root_dir = root_dir
        self.make_dirs()
        self._write_mime_type()
        self._write_items()
        self._write_container_xml()
        self._write_content_opf()
        self._write_toc_ncx()
        self.create_archive(root_dir, root_dir + extension)