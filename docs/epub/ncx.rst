Le fichier de navigation NCX
============================

.. py:module:: epub.ncx

.. toctree::
   :maxdepth: 2

Le format NCX a pour but de proposer un format de table des matières, et permet 
de fournir un mécanisme de navigation au travers du document numérique. Dans le 
cas du format Epub, le format NCX n'est pas utilisé entièrement (il est 
notamment plus permissif, et n'utilise pas les éléments "audio").

.. py:class:: Ncx

   Représente le fichier NCX d'un livre numérique. Un fichier NCX est un 
   fichier xml respectant les spécifications de la norme NCX avec les 
   modifications apportées par la spécification Epub.

   .. py:attribute:: xmlns
   
      Namespace utilisé pour le document NCX, dont la valeur devrait toujours 
      être ``u'http://www.daisy.org/z3986/2005/ncx/'``.
   
   .. py:attribute:: version
   
      Version du fichier NCX, dont la valeur devrait toujours être 
      ``u'2005-1'``.
   
   .. py:attribute:: lang
   
      Langue du contenu du fichier NCX.
   
   .. py:attribute:: uid

      Identifiant unique du livre.
   
   .. py:attribute:: depth

      Représente la meta-donnée ``dtb:depth``.

   .. py:attribute:: total_page_count

      Représente la meta-donnée ``dtb:totalPageCount``.

   .. py:attribute:: max_page_number

      Représente la meta-donnée ``dtb:maxPageNumber``.

   .. py:attribute:: generator

      Représente la meta-donnée ``dtb:generator``.

   .. py:attribute:: title
   
      Titre du livre.
   
   .. py:attribute:: authors
   
      Liste des auteurs du livre.
   
   .. py:attribute:: nav_map

      Objet de la classe :class:`NavMap` représentant l'élément ``<navMap>`` du 
      fichier NCX.

   .. py:attribute:: page_list
   
      Objet de la classe :class:`PageList` représentant l'élément ``<pageList>`` 
      du fichier NCX.
      
   .. py:attribute:: nav_lists = []

      Liste d'objets de la classe :class:`NavList` représentant les éléments 
      ``<navList>`` du fichier NCX.

.. py:class:: NavMap

.. py:class:: PageList

.. py:class:: NavList
