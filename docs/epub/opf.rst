Le fichier OPF
==============

.. py:module:: epub.opf

.. toctree::
   :maxdepth: 2

Open Packaging Format
---------------------

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

Chaque élément du fichier OPF est représenté par une structure permettant 
d'accéder à tous ses éléments, sans avoir à analyser le fichier xml soi-même. 
Ces éléments sont tous renseignés dans les attributs de la classe :class:`Opf` :

* :attr:`Opf.manifest` pour l'élément ``<manifest>``
* :attr:`Opf.metadata` pour l'élément ``<metadata>``
* :attr:`Opf.guide` pour l'élément ``<guide>`` (s'il est présent)
* :attr:`Opf.spine` pour l'élément ``<spine>``

L'élément ``<manifest>``
........................

Cet élément référence la liste des fichiers du livre numérique : textes, 
images, feuilles de style, couverture, etc. ainsi que les `fallback` des 
fichiers qui sortent de la spécification Epub (comme les fichiers PDF).

Vous pouvez obtenir plus d'information directement dans la spécification epub à 
propos de `l'élément manifest`__.

.. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.3

Il est représenté par la classe :class:`Manifest`, et chaque élément du 
manifest est représenté par un objet de la classe :class:`ManifestItem`. En 
outre, la classe :class:`Manifest` peut être utilisée exactement comme un 
``dict`` ne pouvant contenir des objets de type ``ManifestItem``.

Les métadonnées et l'élément ``<metadata>``
...........................................

Les méta-données d'un epub sont renseignés dans l'élément ``<metadata>`` du 
fichier OPF. Pour les représenter, un objet de la classe :class:`Metadata` est 
employé.

La description de chacune de ces meta-données est disponible dans la 
`spécification Epub, section "Metadata"`__.

.. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.2

Comme la pluspart des meta-données peuvent être renseignées plusieurs fois, les 
attributs de cette classe sont souvent des listes d'éléments (principalement 
des tuples contenant à leur tour de simples chaînes de caractères).

Par exemple, pour l'élément ``<title>`` qui peut se décliner en plusieurs 
langues, voici comment il est possible de l'exploiter :

.. code-block:: python

   # meta est un objet de la classe Metadata contenant plusieurs titres
   for title, lang in meta.titles:
       print u'Le titre en %s est "%s"' % (title, lang)

Chaque attribut est décrit avec la forme de son contenu dans la documentation 
de la classe :class:`Metadata`.

L'élément ``<guide>``
.....................

L'élément ``<guide>`` d'un fichier OPF représente une liste des tables et des 
références du livre, pouvant indiquer la couverture, la table des contenus, des 
illustrations, etc.

Voir aussi la `spécification epub OPF, section "guide"`__

.. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.6

Cet élément est représenté par la classe :class:`Guide`.

L'élément ``<spine>``
.....................

L'élément ``<spine>`` propose une liste de fichiers dans un ordre de lecture 
dit "linéaire", c'est à dire dans l'ordre de lecture logique.

La `spécification epub OPF, section "spine"`__ donne plus d'information au 
sujet de cet élément.

.. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4

C'est aussi à partir de cet élément que l'on obtient l'identifiant du fichier 
de navigation NCX, qui permet de retrouver le fichier dans la liste du manifest.

Cet élément est représenté par la classe :class:`Spine`.

Manipuler le fichier OPF
------------------------

En connaissant la structure d'un fichier OPF, structure décrite dans la 
spécification Epub pour le format OPF, il est plutôt simple d'exploiter les 
données proposées par la classe :class:`Opf`.

Cependant, lire une spécification entière n'est pas forcément nécessaire... 
passons à des explications concrètes : comment manipuler un fichier OPF avec 
le module :mod:`epub.opf` ?

Ouvrir et analyser un fichier OPF
.................................

Le plus simple est d'utiliser la fonction :func:`parse_opf`, en lui fournissant 
le contenu du fichier, sous forme d'une chaîne de caractère. Cette fonction 
retourne alors un objet :class:`Opf` qu'il suffit d'utiliser.

Cet objet permet d'accéder aux différents éléments via ses attributs : 
:attr:`metadata <Opf.metadata>`, :attr:`manifest <Opf.manifest>`, 
:attr:`spine <Opf.spine>`, et :attr:`guide <Opf.guide>`.

Obtenir la liste des fichiers
.............................

C'est l'élément ``<manifest>`` qui propose ces informations, il est représenté 
par un objet de la classe :class:`Manifest`, classe qui étend le comportement 
du type ``dict`` :

.. code-block:: python

   # manifest est un objet de la classe epub.opf.Manifest
   for id in manifest:
       # item est un objet de la classe ManifestItem
       item = manifest[id]
       print 'Fichier Id : "%s" [href="%s"]' % (item.id, item.href)

À partir d'un objet de la classe :class:`ManifestItem`, un objet de la classe 
:class:`epub.EpubFile` peut retrouver le contenu associé, grâce à sa méthode 
:meth:`epub.EpubFile.read`.

Les meta-données
................

La classe :class:`Metadata` permet de représenter et donc de manipuler les 
meta-données d'un fichier epub : chacun de ses attributs représente un type de 
meta-données.

Les règles suivantes s'appliquent à tous les attributs composés de plusieurs 
éléments :

* La valeur d'une meta-donnée est représentée par un tuple de ses attributs, 
  chacun représenté par une chaîne de caractère
* Une meta-donnée peut être présente plusieurs fois avec des valeurs 
  différentes : chacune est alors stockée dans une liste
* Un attribut qui n'est pas renseigné dans le fichier xml est représenté par 
  une chaîne vide.

Ainsi, l'attribut :attr:`titles` est une ``list`` de ``tuple`` de la forme 
``(title, lang)``.

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

Utiliser l'élélement ``<spine>``
................................

L'élément ``<spine>`` ne fournit pas directement une liste de fichiers, mais y 
fait seulement référence par l'identifiant de ces fichiers.

.. code-block:: python

   # spine est un objet de la classe epub.opf.Spine
   for id, linear in spine.itemrefs:
       # item est un objet de la classe ManifestItem
       item = book.get_item(id)
       print 'Fichier Id : "%s" [href="%s"]' % (item.id, item.href)

API du module
-------------

La fonction ``parse_opf``
.........................

.. py:function:: parse_opf(xml_string)

   Analyse les données xml au format OPF, et retourne un objet de la classe 
   :class:`Opf` représentant ces données.
   
   :param string xml_string: Le contenu du fichier xml OPF.
   :rtype: Opf

La classe ``Opf``
.................

.. py:class:: Opf(uid_id=None, version=u'2.0', xmlns=XMLNS_OPF, metadata=None, manifest=None, spine=None, guide=None)

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

La classe Metadata
..................

.. py:class:: Metadata()

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

   L'élément ``<dc:rights>``, représenté par une chaîne de caractère.

   .. py:attribute:: metas

   Liste des éléments ``<dc:meta>`` des meta-données. Chaque élément de la 
   liste est un tuple de la forme ``(name, content)``.

Les classes Manifest et ManifestItem
....................................

.. py:class:: Manifest()

   La classe :class:`Manifest` étend le type ``dict`` et peut donc être 
   utilisé de la même façon. Cependant, lorsqu'un élément est inséré dans le 
   dictionnaire, il est vérifié que l'élément en question dispose d'au moins 
   deux attributs nécessaires : ``id`` et ``href``.
   
   Il est préférable de ne stocker que des objets de la classe 
   :class:`ManifestItem`, qui correspond à un usage "normal".
   
   La clé d'accès à chaque élément est la valeur de son attribut ``id``, ce qui 
   permet de retrouver rapidement un objet dans le manifest, exemple :
   
   .. code-block:: python
      
      # manifest is an epub.opf.Manifest object
      item = manifest[u'chap001']
      print item.id # display "chap001"
      
      item in manifest # Return true
      
      # raise a Value Error (key != item.id)
      manifest['bad_id'] = item

   .. py:method:: add_item(id, href, media_type=None, fallback=None, required_namespace=None, required_modules=None, fallback_style=None)
    
      Crée et ajoute un élément au manifest.
      
      Cette méthode n'ajoute rien d'autre qu'une référence à un fichier, mais 
      en aucun cas ne permet d'ajouter concrètement un fichier à l'archive 
      epub : la classe OPF permet de gérer uniquement le fichier XML, et ne se 
      préoccupe donc pas du contenu réel du fichier epub.
    
      :param string id: Identifiant
      :param string href: Chemin d'accès du fichier, relatif à l'emplacement du fichier OPF
      :param string media_type: Le mime-type de l'élément.
      :param string fallback: Identifiant de l'élément fallback
      :param string required_namespace: voir spec epub "required-namespace"
      :param string required_module: voir spec epub "required-module"
      :param string fallback_style: Identifiant de l'élément de style en fallback.

   .. py:method:: append(item)
    
      Ajoute un élément au manifest. Cet élément doit avoir au moins deux 
      attributs : ``id`` et ``href``. L'attribut ``id`` doit être un 
      ``hashable``, c'est à dire un objet immuable permettant de l'utiliser 
      comme clé d'un dictionnaire (comme une chaîne de caractères).
      
      :param epub.opf.ManifestItem item: l'élément à ajouter au manifest

   .. py:method:: as_xml_element()
    
      Retourne un élément xml ``<manifest>`` équivalent au contenu de l'objet.
    
      :rtype: :class:`xml.dom.Element`

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

Les classes Guide et Spine
..........................

.. py:class:: Guide

   .. py:attribute:: references
   
      Liste des références de l'élément ``<guide>``. Chaque élément de la liste 
      est un ``tuple`` de la forme ``(href, type, title)``.
      
      La valeur de ``href`` est une url d'accès relative à l'emplacement du 
      fichier OPF. Cependant, cette url ne peut pas être utilisée directement 
      par les méthodes :meth:`epub.EpubFile.get_item_by_href` ou 
      :meth:`epub.EpubFile.read`, car il peut comporter une ancre (le 
      caractère ``#`` suivit d'un identifiant d'ancre).
   
   .. py:method:: add_reference(href, type=None, title=None)
   
      Ajoute une référence au guide.
    
      :param string href: Chemin d'accès du fichier, relatif à l'emplacement du fichier OPF, peut contenir une ancre
      :param string type: Le type de fichier (voir la spécification epub)
      :param string title: Titre de la référence

   .. py:method:: append(reference)
    
      Ajoute une référence au guide ; elle doit être un tuple de la forme
      ``(href, type, title)``.
       
      :param tuple reference: la référence à ajouter.

.. py:class:: Spine

   .. py:attribute:: itemrefs
   
      Liste des items du manifest référencés par l'ordre de lecture de 
      l'élément ``<spine>``. Les items sont dans l'ordre naturel de la liste 
      (c'est à dire que l'élement présent en première position est le premier 
      dans l'ordre de lecture).
      
      Chaque élement est un ``tuple`` de la forme ``(idref, linear)``. La 
      valeur de ``idref`` est une chaîne de caractère indiquant l'identifiant 
      du fichier listé dans le manifest, et ``linear`` est un booléen indiquant 
      si l'élément sort du flux de lecture "linéaire" (voir la spécification 
      epub pour plus d'information à ce sujet).
   
   .. py:attribute:: toc
      
      Chaîne de caractère : il s'agit de l'identifiant permettant de récupérer 
      le fichier de navigation NCX dans la liste des fichiers du manifest.

   .. py:method:: append(itemref):
    
      Ajoute une référence au spine ; elle doit être un tuple de la forme
      ``(id, linear)``. L'élément est ajouté à la suite des autres.
       
      :param tuple itemref: la référence à ajouter.

   .. py:method:: add_itemref(idref, linear=True)
   
      Ajoute un élément au spine, à la suite des autres déjà présents.
      
      :param string idref: l'identifiant de l'élément à ajouter
      :param bool linear: indicateur d'élément linéaire (par défaut) ou non



