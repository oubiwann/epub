# -*- coding: utf-8 -*-
from __future__ import unicode_literals


def get_node_text(node):
    """
    Return the text content of an xml.dom Element Node.

    If node does not have content, this function return an empty string.
    """
    text = ''

    node.normalize()
    if node.firstChild and node.firstChild.data:
        text = node.firstChild.data.strip()

    return text
