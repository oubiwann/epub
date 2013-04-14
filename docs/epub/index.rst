Le fichier Epub
===============

.. py:module:: epub

.. toctree::
   :maxdepth: 2

Introduction
------------

Pour manipuler un fichier epub, il est nécessaire d'en comprendre la structure. 
Cela n'a rien de bien compliqué en réalité : il s'agit simplement d'une archive 
zip, avec une structure de contenu un peu particulière, et quelques règles 
supplémentaires sur le contenu (format, style, etc.).

Lorsque vous souhaitez lire un fichier epub, vous devez commencer par l'ouvrir 
comme un fichier zip, puis rechercher les fichiers importants qui vous 
permettront de naviguer au travers (le fichier `OPF` d'une part, et le fichier 
de navigation `NCX` d'autre part).

Le module :mod:`epub` vous permet de vous abstraire d'une grosse partie du 
travail d'analyse de cette structure, en fournissant des objets contenant ces 
informations.

Cependant, pour plus de facilité, il est vivement recommandé de connaître un 
minimum la `spécification Epub 2`__, disponible en ligne sur le site de l'IDPF.

.. __: http://idpf.org/epub/201


Ouvrir un fichier Epub
----------------------

La fonction principale du module est :func:`epub.open_epub`, qui permet d'ouvrir 
un fichier epub et d'obtenir un objet de la classe :class:`EpubFile`, 
permettant de manipuler les données du fichier : son contenu et ses 
meta-données.

Elle s'utilise très simplement en lui fournissant le chemin d'accès (relatif 
ou absolu) du fichier epub à ouvrir, et retourne un objet de la classe 
:class:`epub.EpubFile` représentant l'archive epub ainsi ouverte.

On parle ici "d'archive epub", car un fichier epub n'est ni plus ni moins qu'un 
fichier zip avec une structure un peu particulière. Tous les détails de cette 
utilisation du format zip se trouvent dans la `spécification epub`__ (et plus 
spécifiquement dans la spécification OCF).

.. __: http://idpf.org/epub/201

De plus, l'objet :class:`EpubFile` implémentant les bonnes méthodes, vous 
pouvez utiliser la fonction :func:`open_epub` avec l'instruction ``with`` :

.. code-block:: python

   with epub.open_epub('path/to/my_book.epub') as book:
       print 'Vous pouvez lire votre livre !'


Lire le contenu du fichier
--------------------------

Suivant la norme Epub 2, le contenu du fichier epub est décrit par le fichier 
opf, indiqué par le fichier ``META-INF/container.xml``. Si :func:`open_epub` se 
charge de le trouver pour vous, il vous reste à exploiter la liste des fichiers.

Pour se faire, vous pouvez, au choix, utiliser les informations du fichier opf
(via l'attribut :attr:`EpubFile.opf`), ou les informations du fichier ncx (via 
l'attribut :attr:`EpubFile.toc`).

Par exemple pour accéder à l'ensemble des items du fichier :

.. code-block:: python

   book = epub.open_epub('book.epub')
   
   for item in book.opf.manifest.values():
       # read the content
       data = book.read_item(item)

Il est possible d'accéder à l'ordre linéaire des éléments en utilisant 
l'objet de la classe :attr:`opf.Spine` disponible de cette façon :

.. code-block:: python

   book = epub.open_epub('book.epub')
   
   for item_id, linear in book.opf.spine.itemrefs:
       item = book.get_item(item_id)
       # Check if linear or not
       if linear:
           print 'Linear item "%s"' % item.href
       else:
           print 'Non-linear item "%s"' % item.href
       # read the content
       data = book.read_item(item)

Quant au fichier de navigation NCX, il est accessible via l'attribut 
:attr:`EpubFile.toc`. Cet attribut est de la classe :class:`ncx.Ncx` et 
représente le fichier de navigation du livre numérique, et propose une 
structure logique de lecture des fichiers (mais cela demande une connaissance 
plus approfondie de la structure d'un fichier epub).


Écrire dans un fichier epub
---------------------------

Nouveauté de la version 0.4.0, vous pouvez aussi ouvrir un fichier epub en mode
écriture. Le mode `w` permet d'ouvrir un fichier epub vierge, et le mode `a`
d'ajouter du contenu à un fichier epub existant.

Pour le moment, vous ne pouvez qu'ajouter du contenu à un fichier epub, et pas
en retirer.

.. code-block:: python

   book = epub.open_epub('book.epub', u'w')
   filename = 'path/to/file/to/add.xhtml'
   manifest_item = epub.opf.ManifestItem(identifier='IdFile',
                                         href='path/into/epub/add.xhtml',
                                         media_type='application/xhtml+xml')
   book.add_item(filename, manifest_item)
   book.close()

Ce petit exemple vous montre le fonctionnement, qui reste très basique.

Le contenu du fichier epub est réellement sauvegardé lorsqu'il est fermé, c'est
à dire à l'appel de la méthode :meth:`epub.EpubFile.close`.


API du module
-------------

La fonction open_epub
.....................

.. py:function:: open_epub(filename, mode='r')
   
   Ouvre un fichier epub, et retourne un objet :class:`epub.EpubFile`. Vous
   pouvez ouvrir le fichier en lecture seule (mode `r` par défaut) ou en
   écriture (mode `w` ou mode `a`).
   
   Il est possible d'utiliser cette fonction avec la directive ``with`` de 
   cette façon :
   
   .. code-block:: python
      
      with epub.open_epub('path/to/my.epub') as book:
          # do thing with book, for exemple:
          print book.read_item('Text/cover.xhtml')
   
   Le mode d'écriture `w` ouvre le fichier epub en écriture et considère un
   fichier vierge. Si le fichier existe déjà il est remplacé.
   
   Le mode d'écriture `a` ouvre le fichier epub en écriture et permet de
   modifier un fichier déjà existant. Si le fichier n'existe pas, il est créé
   et traité de la même façon qu'avec le mode `w`.
   
   :param string filename: chemin d'accès au fichier epub

La classe EpubFile
..................

.. py:class:: EpubFile(filename)

   Cette classe représente le contenu d'un fichier au format Epub. Elle permet 
   de représenter tant les meta-données (le fichier OPF) que la navigation (le 
   fichier NCX).
   
   Les éléments du fichier epub ne sont pas tous directement accessibles : il 
   faut passer par les attributs :attr:`opf <epub.EpubFile.opf>` et 
   :attr:`toc <epub.EpubFile.toc>`.
   
   Il est préférable d'utiliser la fonction :func:`epub.open_epub` plutôt 
   qu'instancier directement un objet EpubFile.

   .. py:attribute:: EpubFile.opf

      Objet de la classe :class:`Opf <epub.opf.Opf>` représentant le fichier 
      opf.

   .. py:attribute:: EpubFile.opf_path

      Chemin d'accès interne à l'archive zip au fichier OPF.

      Le chemin du fichier OPF est spécifié par le fichier 
      ``META-INF/container.xml`` et ce chemin est conservé dans cet attribut. 
      L'emplacement sert de référence à l'emplacement des autres fichiers du 
      livre (html, styles, images, etc.).

   .. py:attribute:: EpubFile.toc

      Le sigle "toc" signifie "Table Of Content", et cet attribut représente le 
      fichier ncx décrivant cette table des matières.

      Il s'agit d'un objet de la classe :class:`Ncx <epub.ncx.Ncx>`, qui peut 
      être accéder directement pour en utiliser le contenu.

   .. py:attribute:: EpubFile.uid

      Identifiant unique du fichier epub. Cet identifiant peut être un ISBN ou 
      un autre format d'identifiant unique.
      
      Le format de cet attribut est un tuple, contenant trois éléments :
      
      * la valeur de l'identifiant unique (``uid[0]``)
      * l'identifiant associé dans le fichier OPF (``uid[1]``)
      * le schéma tel que défini par l'attribut ``opf::scheme`` (``uid[2]``)

      Cet identifiant peut être retrouvé dans la liste des identifiants via les 
      meta-données (voir aussi :attr:`epub.opf.Metadata.identifiers`).

   .. py:method:: __init__(file)
   
      Initialise l'objet :class:`epub.EpubFile`. 

   .. py:method:: add_item(filename, manifest_item)
   
      Permet d'ajouter un fichier au livre numérique. 
      
      Le premier paramètre indique le fichier source (le contenu), et le second
      indique les meta-données à ajouter au fichier OPF, dont l'emplacement 
      dans l'archive epub.
      
      L'attribut `id` du `manifest_item` ne doit pas déjà exister dans le
      fichier epub.
      
      L'attribut `href` du `manifest_item` doit être un chemin d'accès relatif
      à l'emplacement du fichier OPF.
   
      :param string filename: Le chemin d'accès au fichier à ajouter.
      :param epub.opf.ManifestItem manifest_item: l'item décrivrant le fichier
       à ajouter pour le fichier OPF.
      :raise RuntimeError: Si le fichier est déjà clos.
      :raise IOError: Si le fichier n'est pas ouvert en écriture.

   .. py:method:: check_mode_write()
   
      Lève une exception si le fichier n'est pas ouvert en mode écriture (`w`
      ou `a`), ou si le fichier est déjà clos et qu'il ne peut être modifié.

      :raise RuntimeError: Si le fichier est déjà clos.
      :raise IOError: Si le fichier n'est pas ouvert en écriture.

   .. py:method:: close()
   
      Ferme le fichier epub. S'il était ouvert en mode écriture (`w` ou `a`),
      alors le fichier OPF et le fichier NCX sont générés en XML et modifié
      dans l'archive epub avant la fermeture.
      
      L'appel à cette méthode assure la sauvegarde des modifications effectuées.

   .. py:method:: extract_item(item[, to_path=None])

      Extrait le contenu d'un fichier présent dans l'archive epub à
      l'emplacement indiqué par `to_path`. Si `to_path` vaut `None` alors le
      fichier est extrait à l'emplacement de travail courrant.

      Le paramètre ``item`` peut être un objet :class:`epub.opf.ManifestItem` 
      ou un chemin d'accès du fichier, chemin relatif à l'emplacement du 
      fichier OPF.

      Ce chemin ne doit pas contenir de fragment d'url (commençant pas `#`).

      Voir aussi la méthode :meth:`zipfile.ZipFile.Extract` sur laquelle
      repose le comportement de cette méthode.
 
      http://docs.python.org/library/zipfile.html#zipfile.ZipFile.extract

      :param mixed item: Le chemin ou le Manifest Item.
      :param string to_path: Le chemin où extraire le fichier (par défaut il
          s'agit du répertoire de travail courrant).

   .. py:method:: EpubFile.get_item(identifier)
 
      Cette fonction permet de récupérer un "item" du manifest. Le fichier opf 
      décrit, via son "manifest", une liste des fichiers composant le livre 
      numérique : chacun de ces éléments est un "item", qui représente l'un des 
      fichier de l'epub.

      :param string identifier: Identifiant de l'item recherché.
      :rtype: :class:`epub.opf.ManifestItem` ou ``None`` s'il n'existe pas.

   .. py:method:: EpubFile.get_item_by_href(href)

      Fonctionne de la même façon que :meth:`get_item <EpubFile.get_item>` en 
      utilisant la valeur de l'attribut `href` des items du manifest.

      :param string href: Chemin d'accès (relatif au fichier opf) de l'item recherché.
      :rtype: :class:`epub.opf.ManifestItem` ou ``None`` s'il n'existe pas.

   .. py:method:: EpubFile.read_item(item)

      Retourne le contenu d'un fichier présent dans l'archive epub.
      
      Le paramètre ``item`` peut être un objet :class:`epub.opf.ManifestItem` 
      ou un chemin d'accès du fichier, chemin relatif à l'emplacement du 
      fichier OPF.
      
      Ce chemin ne doit pas contenir de fragment d'url (commençant pas `#`).

      Voir aussi la méthode :meth:`zipfile.ZipFile.read`.

      http://docs.python.org/library/zipfile.html#zipfile.ZipFile.read

      .. code-block:: python
      
         book = epub.open_epub('mybook.epub')
      
         # get chapter 1
         item = book.get_item('chap01')
         item_path = item.href # 'Text/chap01.xhtml'
         
         # display the same thing
         print book.read_item(item)
         print book.read_item(item_path)
         
         # but this won't work!
         content = book.read_item('Text/chap01.xhtml#part1')
      
      :param mixed item: Le chemin ou le Manifest Item.
      :rtype: string

La classe Book
..............

.. py:class:: Book

   Cette classe permet de simplifier l'accès en lecture à un fichier epub.
   Un objet Book sert de proxy à l'objet plus complexe EpubFile, par un
   ensemble de `@property` adaptées.
