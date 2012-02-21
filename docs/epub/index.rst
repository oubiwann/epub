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

La fonction principale du module est :func:`epub.open`, qui permet d'ouvrir 
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
pouvez utiliser la fonction :func:`open` avec l'instruction ``with`` :

.. code-block:: python

   with epub.open('path/to/my_book.epub') as book:
       print 'Vous pouvez lire votre livre !'

Lire le contenu du fichier
--------------------------

Suivant la norme Epub 2, le contenu du fichier epub est décrit par le fichier 
opf, indiqué par le fichier ``META-INF/container.xml``. Si :func:`open` se 
charge de le trouver pour vous, il vous reste à exploiter la liste des fichiers.

Pour se faire, vous pouvez, au choix, utiliser les informations du fichier opf
(via l'attribut :attr:`EpubFile.opf`), ou les informations du fichier ncx (via 
l'attribut :attr:`EpubFile.toc`).

Par exemple pour accéder à l'ensemble des items du fichier :

.. code-block:: python

   book = epub.open('book.epub')
   
   for item in book.opf.manifest.items:
       # read the content
       data = book.read(item)

.. warning::

   Cette façon de parcourir la liste des éléments est soumise à de très 
   probables changements futur, car pour le moment, cette méthode reste trop 
   peu intuitive pour être satisfaisante.
   
   De plus, il reste tout à fait possible d'utiliser le fichier de navigation 
   ncx, dont la structure logique sera sans doute bien plus approprié quoi 
   qu'il arrive à la façon d'accéder aux fichiers.
   
   En outre, les méthodes :meth:`EpubFile.get_item` et 
   :meth:`EpubFile.get_item_by_href` continueront de retourner les éléments 
   demandés en prenant les mêmes paramètres. `Tout n'est pas perdu.`

Il est possible d'accéder à l'ordre linéaire des éléments en utilisant 
l'objet de la classe :attr:`opf.Spine` disponible de cette façon :

.. code-block:: python

   book = epub.open('book.epub')
   
   for item_id, linear in book.opf.spine.itemrefs:
       item = book.get_item(item_id)
       # Check if linear or not
       if linear:
           print u'Linear item "%s"' % item.href
       else:
           print u'Non-linear item "%s"' % item.href
       # read the content
       data = book.read(item)

Quant au fichier de navigation NCX, il est accessible via l'attribut 
:attr:`EpubFile.toc`. Cet attribut est de la classe :class:`ncx.Ncx` et 
représente le fichier de navigation du livre numérique, et propose une 
structure logique de lecture des fichiers.

API du module
-------------

La fonction open
................

.. py:function:: open(filename)
   
   Ouvre un fichier epub, et retourne un objet :class:`epub.EpubFile`.
   
   :param string filename: chemin d'accès au fichier epub

La classe EpubFile
..................

.. py:class:: EpubFile([zip])

   Cette classe représente le contenu d'un fichier au format Epub. Elle permet 
   de représenter tant les meta-données (le fichier OPF) que la navigation (le 
   fichier NCX).
   
   Les éléments du fichier epub ne sont pas tous directement accessibles : il 
   faut passer par les attributs :attr:`opf <epub.EpubFile.opf>` et 
   :attr:`toc <epub.EpubFile.toc>`.
   
   Il est possible de fournir l'archive zip directement à l'instanciation de 
   l'objet Epub. Le mieux est cependant d'utiliser la fonction 
   :func:`epub.open` du module.

   .. py:attribute:: EpubFile.opf_path

      Chemin d'accès interne à l'archive zip au fichier OPF.

      Le chemin du fichier OPF est spécifié par le fichier 
      ``META-INF/container.xml`` et ce chemin est conservé dans cet attribut.
      
   .. py:attribute:: EpubFile.opf

      Objet de la classe :class:`Opf <epub.opf.Opf>` représentant le fichier 
      opf.

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

   .. py:attribute:: EpubFile.zip

      Objet de la classe :class:`zipfile.ZipFile` représentant l'archive zip 
      qui contient les données concrètes du fichier epub.

   .. py:method:: EpubFile.get_item(id)
 
      Cette fonction permet de récupérer un "item" du manifest. Le fichier opf 
      décrit, via son "manifest", une liste des fichiers composant le livre 
      numérique : chacun de ces éléments est un "item", qui représente l'un des 
      fichier de l'epub.
      
      :param string id: Identifiant de l'item recherché.
      :rtype: :class:`epub.opf.ManifestItem` ou ``None`` s'il n'existe pas.

   .. py:method:: EpubFile.get_item_by_href(href)

      Fonctionne de la même façon que :meth:`get_item <EpubFile.get_item>`
   
      :param string href: Chemin d'accès (relatif au fichier opf) de l'item recherché.
      :rtype: :class:`epub.opf.ManifestItem` ou ``None`` s'il n'existe pas.

   .. py:method:: EpubFile.read(item)
   
      Retourne le contenu d'un fichier présent dans l'archive epub.
      
      Le paramètre ``item`` peut être un objet :class:`epub.opf.ManifestItem` 
      ou un chemin d'accès du fichier, chemin relatif à l'emplacement du 
      fichier OPF.

      .. code-block:: python
      
         book = epub.open('mybook.epub')
      
         # get chapter 1
         item = book.get_item('chap01')
         item_path = item.href # u'Text/chap01.xhtml'
         
         # display the same thing
         print book.read(item)
         print book.read(item_path)
         
         # but this won't work!
         content = book.read(u'Text/chap01.xhtml#part1')
      
      :rtype: string

   .. py:method:: EpubFile.close()
   
      Ferme l'archive epub : le fichier epub n'étant qu'une archive zip, il 
      s'agit là de l'appel à la méthode 
      :meth:`close() <zipfile.ZipFile.close>` de l'attribut 
      :attr:`zip <epub.EpubFile.zip>`.
      
      Cette méthode n'est actuellement pas très utile, car l'archive zip est 
      toujours ouverte en lecture seule, il n'y a donc aucun changement à 
      valider par la fermeture de l'archive zip.

