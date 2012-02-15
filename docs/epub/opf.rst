Documentation du module epub.opf
================================

.. py:module:: epub.opf

.. toctree::
   :maxdepth: 2

Le fichier OPF
--------------

Le format OPF (pour `Open Packaging Format`) spécifié par l'IDPF permet 
d'indiquer au système de lecture quelle est la structure et le contenu d'un 
fichier epub.

Ses principaux composants sont ses meta-données et son élément ``<manifest>``, 
ce dernier référençant les fichiers qui composent effectivement le livre 
numérique.

Différents éléments annexes sont aussi présents : l'élément ``<spine>`` qui 
donne un ordre de lecture linéaire, et l'élément ``<guide>`` qui référence les 
différentes tables des matières, des illustrations, etc.

La bibliothèque python-epub propose un module à part entière pour manipuler ce 
format (dans sa version pour Epub 2.0), permettant une plus grande souplesse 
dans son utilisation.

.. py:function:: parse_opf(xml_string)

   :param string xml_string

.. py:class:: Opf(uid_id=None, version=u'2.0', xmlns=XMLNS_OPF, metadata=None, manifest=None, spine=None, guide=None)

   Le format OPF permet de décrire le contenu d'un fichier epub : il décrit non 
   seulement les méta-données (titres, auteurs, etc.) mais aussi la liste des 
   fichiers qui représentent le contenu du livre.
   
   :param epub.opf.Metadata metadata: Les méta-données du fichier OPF
   :param epub.opf.Manifest manifest: L'élélement manifest du fichier OPF
   :param epub.opf.Spine spine: L'élément spine du fichier OPF
   :param epub.opf.Guide guide: L'élément guide du fichier OPF

   .. py:attribute:: uid_id
   
      Identifiant de l'identifiant unique du livre numérique. L'identifiant 
      ainsi référencé est disponible dans la liste des identifiants des 
      méta-données (voir l'attribut :attr:`metadata` et son attribut 
      :attr:`Metadata.identifiers`).
   
   .. py:attribute:: version
   
      Indique la version du fichier opf (2.0 par défaut), sous la forme d'une 
      chaîne de caractère.
   
   .. py:attribute:: xmlns
   
      Indique le namespace du fichier OPF. Cette valeur ne devrait pas être 
      modifiée.
      
      Sa valeur par défaut est ``http://www.idpf.org/2007/opf``.
   
   .. py:attribute:: metadata
   
      Représente les méta-données du fichier epub, sous la forme d'un objet de 
      la classe :class:`Metadata`.
   
   .. py:attribute:: manifest
   
      Objet de la classe :class:`Manifest` représentant la balise 
      ``<manifest>`` du fichier OPF référençant les fichiers du livre 
      numérique.
   
   .. py:attribute:: spine
   
      Objet de la classe :class:`Spine` représentant la balise ``<spine>`` du 
      fichier OPF indiquant un ordre de lecture linéaire. 
      
   .. py:attribute:: guide
   
      Objet de la classe :class:`Guide` représentant la balise ``<guide>`` du 
      fichier OPF indiquant une liste de références (tables de contenus, 
      d'illustration, etc.).

L'élément ``<manifest>``
------------------------

.. py:class:: Manifest()

   Représente l'élément ``<manifest>`` d'un fichier OPF.

   Cet élément référence la liste des fichiers du livre numérique : textes, 
   images, feuilles de style, couverture, etc. ainsi que les `fallback` des 
   fichiers qui sortent de la spécification Epub (comme les fichiers PDF).

   La spécification epub à propos de `l'élément manifest`__.
   
   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.3

   .. py:attribute:: items
   
      Cet attribut est une liste, contenant les fichiers référencés par le 
      manifest de l'epub. Chaque élément de cette liste est un objet de la 
      classe :class:`ManifestItem`

   .. py:method:: add_item(id, href, media_type=None, fallback=None, required_namespace=None, required_modules=None, fallback_style=None)
    
      Crée et ajoute un élément au manifest.
      
      Cette méthode n'ajoute rien d'autre qu'une référence à un fichier, mais 
      en aucun cas ne permet d'ajouter concrètement un fichier à l'archive 
      epub : la classe OPF permet de gérer uniquement le fichier XML, et ne se 
      préoccupe donc pas du contenu réel du fichier epub.
    
      :param string id: Identifiant
      :param string href: Chaine de caractère
      :param string media_type: Le mime-type de l'élément.
      :param string fallback: Identifiant de l'élément fallback
      :param string required_namespace: voir spec epub "required-namespace"
      :param string required_module: voir spec epub "required-module"
      :param string fallback_style: Identifiant de l'élément de style en fallback.

   .. py:method:: append(item)
    
      Ajoute un élément au manifest.
      
      :param epub.opf.ManifestItem item: l'élément à ajouter au manifest

.. py:class:: ManifestItem(id, href, media_type=None, fallback=None, required_namespace=None, required_modules=None, fallback_style=None)

   Un objet de la classe :class:`ManifestItem` représente un élément du 
   manifest du fichier epub, c'est à dire l'un des fichiers qui compose le 
   livre numérique.
   
   Chacun de ses attributs représente l'un des attributs de l'élément 
   ``<item>`` tel qu'il est décrit par la spécification epub.
   
   .. code-block:: python

      """
      <item id="chap01" href="Text/chap01.xhtml" media-type="application/xhtml+xml"/>
      """
      
      # equivalent metadata
      item = epub.opf.ManifestItem()
      item.id = u'chap01'
      item.href = u'Text/chap01.xhtml'
      item.media_type = u'application/xhtml+xml'
      
      # ou bien directement avec le constructeur
      item = epub.opf.ManifestItem(id=u'chap01', href=u'Text/chap01.xhtml',
                                   media_type=u'application/xhtml+xml')
   
   .. py:attribute:: id
   
      Identifiant de l'item, qui doit être unique pour permettre de récupérer 
      chaque élément dans la liste des items du manifest.
      
      Il s'agit d'une chaîne de caractère.
      
   .. py:attribute:: href
   
      Chemin d'accès au fichier présent dans l'archive zip. Ce chemin d'accès 
      est relatif à l'emplacement du fichier opf dans lequel est décrit l'item.
   
   .. py:attribute:: media_types
   
      Chaîne de caractère, indique le mime-type du fichier correspondant à 
      l'item.
   
   .. py:attribute:: fallback
   
      Chaîne de caractère, indique l'identifiant de l'item servant de 
      `fallback` à cet item (ce mécanisme est décrit dans la spécification 
      epub).
   
   .. py:attribute:: required_namespace
   
      Chaîne de caractère, indique le namespace pour les élements `"Out-of-Line 
      XML Island"`.
   
   .. py:attribute:: required_modules
   
      Chaîne de caractère, indique le ou les modules pour les élements 
      `"Out-of-Line XML Island"`.
      
   .. py:attribute:: fallback_style
   
      Indique l'identifiant de l'item servant de `fallback` pour la feuille de 
      style à cet item (ce mécanisme est décrit dans la spécification epub).

   .. py:method:: as_xml_element()
      
      Créer un ``Element Node`` représentant l'objet avec ses attributs. Un 
      attribut dont la valeur est ``None`` ou une chaîne vide ne sera pas 
      ajouté à l'élément xml retourné (il ne crée pas d'attribut vide).
      
      :rtype: :class:`xml.dom.Element`

Les métadonnées et l'élément ``<metadata>``
-------------------------------------------

.. py:class:: Metadata()

   Cette classe permet de représenter les meta-données décrites dans le fichier 
   OPF du fichier epub, contenu dans la balise ``<metadata>``. La description 
   de chacune de ces meta-données est disponible dans la `spécification Epub, 
   section "Metadata"`__.

   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.2

   Les règles suivantes s'appliquent à tous les attributs composés de plusieurs 
   éléments :

   * La valeur d'une meta-donnée est représentée par un tuple de ses attributs, 
     chacun représenté par une chaîne de caractère
   * Une meta-donnée peut être présente plusieurs fois avec des valeurs 
     différentes : chacune est alors stockée dans une liste
   * Un attribut qui n'est pas renseigné dans le fichier xml est représenté par 
     une chaîne vide.

   Ainsi, l'attribut :attr:`titles` est une ``list`` de ``tuple`` de la 
   forme ``(title, lang)``.

   Les autres attributs simples sont représentées par une chaîne de caractères.

   .. code-block:: python

      """
      <metadata>
          <dc:title xml:lang="fr">Titre français</dc:title>
          <dc:title xml:lang="en">English title</dc:title>
      </metadata>
      """
      
      # equivalent metadata
      metadata = epub.opf.Metadata()
      metadata.title = [(u'Titre français', u'fr'), (u'English title', u'en')]

   .. py:attribute:: titles

   Liste des éléments ``<dc:title>`` des meta-données. Chaque élément de la 
   liste est un tuple de la forme ``(title, lang)``.

   .. py:attribute:: creators

   Liste des éléments ``<dc:creator>`` des meta-données. Chaque élément de la 
   liste est un tuple de la forme ``(name, role, file as)``.

   .. py:attribute:: subjects

   Liste des éléments ``<dc:subjet>`` des meta-données. Chaque élément de la 
   liste est une chaîne de caractère représentant la valeur du sujet.

   .. py:attribute:: description

   L'élément ``<dc:description>``, représenté par une chaîne de caractère.

   .. py:attribute:: publisher

   L'élément ``<dc:publisher>``, représenté par une chaîne de caractère.

   .. py:attribute:: contributors

   Liste des éléments ``<dc:contributor>`` des meta-données. Chaque élément de 
   la liste  est un tuple de la forme ``(name, role, file as)``.

   .. py:attribute:: dates

   Liste des éléments ``<dc:date>`` des meta-données. Chaque élément de la 
   liste est un tuple de la forme ``(date, event)``.

   .. py:attribute:: type

   L'élément ``<dc:type>``, représenté par une chaîne de caractère.

   .. py:attribute:: format

   L'élément ``<dc:format>``, représenté par une chaîne de caractère.

   .. py:attribute:: identifiers

   Liste des éléments ``<dc:identifier>`` des meta-données. Chaque élément de 
   la liste est un tuple de la forme ``(uid, id, scheme)``.

   La partie ``id`` est l'identifiant qui permet de référencer quel 
   ``identifier`` doit être utilisé pour définir l'UID de fichier epub.

   .. py:attribute:: source

   L'élément ``<dc:source>``, représenté par une chaîne de caractère.

   .. py:attribute:: languages

   Liste des éléments ``<dc:language>`` des meta-données. Chaque élément de la 
   liste est une chaîne de caractère.

   Plus de précision sur la balise ``<dc:language>`` dans la `spécification 
   epub, section "metadata : language"`__

   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.2.12

   .. py:attribute:: Metadata.relation

   L'élément ``<dc:relation>``, représenté par une chaîne de caractère.

   .. py:attribute:: coverage

   L'élément ``<dc:coverage>``, représenté par une chaîne de caractère.

   .. py:attribute:: right

   L'élément ``<dc:coverage>``, représenté par une chaîne de caractère.

   .. py:attribute:: metas

   Liste des éléments ``<dc:meta>`` des meta-données. Chaque élément de la 
   liste est un tuple de la forme ``(name, content)``.

Les éléments ``<guide>`` et ``<spine>``
---------------------------------------

.. py:class:: Guide

   L'élément ``<guide>`` d'un fichier OPF représente une liste des tables et 
   des références du livre, pouvant indiquer la couverture, la table des 
   contenus, des illustrations, etc.
   
   Voir aussi la `spécification epub OPF, section "guide"`__
   
   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.6

.. py:class:: Spine

   Permet de représenter l'élément ``<spine>`` d'un fichier OPF.
   
   Cet élément indique une liste de fichiers dans un ordre de lecture dit 
   "linéaire", c'est à dire dans l'ordre de lecture logique.

   Voir aussi la `spécification epub OPF, section "spine"`__
   
   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4
