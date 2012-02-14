Documentation du module epub
============================

.. py:module:: epub

.. toctree::
   :maxdepth: 2

La fonction open()
------------------

La fonction principale du module est :func:`epub.open`, qui permet d'ouvrir 
un fichier epub et d'obtenir un objet de la classe ``EpubFile``, permettant de 
manipuler les données du fichier : contenu et meta-données.

.. py:function:: open(filename)
   
   Ouvre un fichier epub, et retourne un objet :class:`epub.EpubFile`.
   
   :param string filename: chemin d'accès au fichier epub

La classe EpubFile
------------------

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
      :rtype: Un objet :class:`epub.opf.ManifestItem` ou ``None`` s'il n'existe pas.

   .. py:method:: EpubFile.get_item_by_href(href)

      Fonctionne de la même façon que :meth:`get_item <EpubFile.get_item>`
   
      :param string href: Chemin d'accès (relatif au fichier opf) de l'item recherché.
      :rtype: Un objet :class:`epub.opf.ManifestItem` ou ``None`` s'il n'existe pas.

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
      
      :rtype: Le contenu du fichier recherché, sous forme d'une chaîne de caractères.

   .. py:method:: EpubFile.close()
   
      Ferme l'archive epub : le fichier epub n'étant qu'une archive zip, il 
      s'agit là de l'appel à la méthode 
      :meth:`close() <zipfile.ZipFile.close>` de l'attribut 
      :attr:`zip <epub.EpubFile.zip>`.
      
      Cette méthode n'est actuellement pas très utile, car l'archive zip est 
      toujours ouverte en lecture seule, il n'y a donc aucun changement à 
      valider par la fermeture de l'archive zip.

