Le fichier de navigation NCX
============================

.. py:module:: epub.ncx

.. toctree::
   :maxdepth: 2

Navigation Center eXtended
--------------------------

Le format NCX est un format XML qui permet de décrire la structure de 
navigation d'un livre numérique. La spécification de ce format est dirigé et 
maintenu par le `DAISY Consortium`__.

.. __: http://www.niso.org/workrooms/daisy/Z39-86-2005.html#NCX

   The Navigation Control file for XML applications (NCX) exposes the 
   hierarchical structure of a Publication to allow the user to navigate 
   through it. The NCX is similar to a table of contents in that it enables the 
   reader to jump directly to any of the major structural elements of the 
   document

Il est employé dans le cadre du format epub avec quelques modifications 
apportées par la `spécification epub OPF`__.

.. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4.1

Tout comme le format OPF, la bibliothèque python-epub propose un module à part 
entière pour manipuler ce format plus simplement.

La classe :class:`Ncx` permet au développeur d'utiliser ce contenu au travers 
de ses différents attributs :

* :attr:`Ncx.nav_map` pour l'élément ``<navMap>``
* :attr:`Ncx.page_list` pour l'élément ``<pageList>``
* :attr:`Ncx.nav_lists` pour les éléments ``<navList>``

Comprendre la structure
.......................

La clé pour comprendre comment utiliser le format NCX est sans doute de 
comprendre le principe d'une table de matière ; prenez l'exemple suivant :

* Volume 1
   * Partie I
      * Chapitre 1
      * Chapitre 2
      * Chapitre 3
   * Partie II
      * Chapitre 1
      * Chapitre 2
      * Chapitre 3

Cette structure est finalement très simple : un arbre aux ramification 
descendantes. Cette liste est une ``<navMap>``, dont chaque élément est un 
``<navPoint>``.

Voici la même chose au format xml :

.. code-block:: xml

   <navMap>
       <navPoint playOrder="1" id="vol1">
           <navLabel><text>Volume 1</text></navLabel>
           <content src="Text/vol1.html"/>
           <navPoint playOrder="2">
               <navLabel><text>Partie I</text></navLabel>
               <content src="Text/vol1/part1.html"/>
               <navPoint playOrder="3">
                   <navLabel><text>Chapitre 1</text></navLabel>
                   <content src="Text/vol1/part1.html#chap1"/>
               </navPoint>
               <navPoint playOrder="4">
                   <navLabel><text>Chapitre 2</text></navLabel>
                   <content src="Text/vol1/part1.html#chap2"/>
               </navPoint>
               <navPoint playOrder="5">
                   <navLabel><text>Chapitre 3</text></navLabel>
                   <content src="Text/vol1/part1.html#chap3"/>
               </navPoint>
           </navPoint>
           <navPoint playOrder="6">
               <navLabel><text>Partie II</text></navLabel>
               <content src="Text/vol1/part2.html"/>
               <navPoint>
                   <navLabel><text>Chapitre 1</text></navLabel>
                   <content src="Text/vol1/part2/chap1.html"/>
               </navPoint>
               <navPoint>
                   <navLabel><text>Chapitre 2</text></navLabel>
                   <content src="Text/vol1/part2/chap2.html"/>
               </navPoint>
               <navPoint>
                   <navLabel><text>Chapitre 3</text></navLabel>
                   <content src="Text/vol1/part2/chap3.html"/>
               </navPoint>
           </navPoint>
       </navPoint>
   </navMap>

Vous aurez sans doute remarqué plusieurs choses :

* L'attribut ``playOrder`` est global : il indique l'ordre de lecture
* Cet attribut est cependant **optionnel**
* Un ``<navPoint>`` représente une entrée de la navigation
* Un ``<navPoint>`` peut avoir lui-même plusieurs ``<navPoint>`` en fils
* Le contenu pointé par un ``<navPoint>``, via sa balise ``<content>`` n'est 
  pas un chemin d'accès mais une url relative à l'emplacement du fichier NCX

Armée de cette nouvelle compréhension, utiliser un objet :class:`Ncx` ne 
devrait plus être un gros problème.

API du module
-------------

La fonction ``parse_ncx``
.........................

.. py:function:: parse_ncx(xml_string)

   Analyse les données xml au format NCX, et retourne un objet de la classe 
   :class:`Ncx` représentant ces données.
   
   :param string xml_string: Le contenu du fichier xml NCX.
   :rtype: Ncx

La classe ``Ncx``
.................

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
      fichier NCX. Cet attribut permet d'accéder à la structure de navigation 
      principale.

   .. py:attribute:: page_list
   
      Objet de la classe :class:`PageList` représentant l'élément ``<pageList>`` 
      du fichier NCX.
      
   .. py:attribute:: nav_lists

      Liste d'objets de la classe :class:`NavList` représentant les éléments 
      ``<navList>`` du fichier NCX.
      
      Il peut n'y avoir aucun élément dans cette liste.

Les classes ``NavMap`` et ``NavPoint``
......................................

.. py:class:: NavMap

   .. py:attribute:: id

      Identifiant de la NavMap. Chaîne de caractère (peut être vide).

   .. py:attribute:: labels

      Liste des labels de la NavMap : chaque label et un tuple de la forme 
      ``(label, lang, dir)``, indiquant respectivement le titre du label, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).

   .. py:attribute:: infos

      Liste des infos de la NavMap : chaque info et un tuple de la forme 
      ``(info, lang, dir)``, indiquant respectivement le contenu de l'info, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).
      
      Une "info" est simplement une description de l'élément.

   .. py:attribute:: nav_point
   
      Liste des éléments ``<navPoint>`` en fils direct de l'élément 
      ``<navMap>`` (et pas ses petits fils). Chaque élément de cette liste est 
      un objet de la classe :class:`NavPoint`.

.. py:class:: NavPoint

   .. py:attribute:: id

      Chaîne de caractère, identifiant du ``<navPoint>``.

   .. py:attribute:: class_name
   
      Chaîne de caractère, indique la classe css proposée.
   
   .. py:attribute:: play_order
   
      Chaîne de caractère, indique le placement dans l'ordre de lecture de 
      l'élément. Peut être vide.
   
   .. py:attribute:: labels
   
      Liste des labels du ``<navPoint>`` : chaque label et un tuple de la forme 
      ``(label, lang, dir)``, indiquant respectivement le titre du label, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).
   
   .. py:attribute:: src
   
      Chaîne de caractère, indique l'url relative à l'emplacement du fichier 
      NCX, et pouvant pointer vers des fragments de fichiers du fichier epub.
      
      Exemple : ``Text/chap1.xhtml#p36`` indique le fichier 
      ``Text/chap1.xhtml`` et plus spéficiquement à l'emplacement du fragment 
      ``p36``.
   
   .. py:attribute:: nav_point
   
      Liste des éléments ``<navPoint>`` fils directs. Chaque élément est un 
      objet de la classe :class:`NavPoint`.

Les classes ``PageList`` et ``PageTarget``
..........................................

.. py:class:: PageList

   .. py:attribute:: id

      Chaîne de caractère, identifiant du ``<pageList>``.

   .. py:attribute:: class_name
   
      Chaîne de caractère, indique la classe css proposée.
   
   .. py:attribute:: labels
   
      Liste des labels du ``<navPoint>`` : chaque label et un tuple de la forme 
      ``(label, lang, dir)``, indiquant respectivement le titre du label, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).

   .. py:attribute:: infos
   
      Liste des infos de la NavMap : chaque info et un tuple de la forme 
      ``(info, lang, dir)``, indiquant respectivement le contenu de l'info, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).
      
      Une "info" est simplement une description de l'élément.

   .. py:attribute:: page_target
   
      Liste des éléments ``<pageTarget>`` fils directs. Chaque élément est un 
      objet de la classe :class:`PageTarget`.

.. py:class:: PageTaget

   .. py:attribute:: id

      Chaîne de caractère, identifiant du ``<pageList>``.

   .. py:attribute:: labels
   
      Liste des labels du ``<navPoint>`` : chaque label et un tuple de la forme 
      ``(label, lang, dir)``, indiquant respectivement le titre du label, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).

   .. py:attribute:: value
   
      Chaîne de caractères, représente l'attribut ``value`` de l'élément.
   
   .. py:attribute:: type
      
      Chaîne de caractères.

   .. py:attribute:: class_name
   
      Chaîne de caractère, indique la classe css proposée.
      
   .. py:attribute:: play_order
   
      Chaîne de caractère, indique le placement dans l'ordre de lecture de 
      l'élément. Peut être vide.
      
   .. py:attribute:: src
   
      Chaîne de caractère, indique l'url relative à l'emplacement du fichier 
      NCX, et pouvant pointer vers des fragments de fichiers du fichier epub.
      
      Exemple : ``Text/chap1.xhtml#p36`` indique le fichier 
      ``Text/chap1.xhtml`` et plus spéficiquement à l'emplacement du fragment 
      ``p36``.


Les classes ``NavList`` et ``NavTarget``
..........................................

.. py:class:: NavList

   .. py:attribute:: id

      Chaîne de caractère, identifiant du ``<navList>``.

   .. py:attribute:: class_name
   
      Chaîne de caractère, indique la classe css proposée.
   
   .. py:attribute:: labels
   
      Liste des labels du ``<navPoint>`` : chaque label et un tuple de la forme 
      ``(label, lang, dir)``, indiquant respectivement le titre du label, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).

   .. py:attribute:: infos
   
      Liste des infos de la NavMap : chaque info et un tuple de la forme 
      ``(info, lang, dir)``, indiquant respectivement le contenu de l'info, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).
      
      Une "info" est simplement une description de l'élément.

   .. py:attribute:: nav_target
   
      Liste des éléments ``<navTarget>`` fils directs. Chaque élément est un 
      objet de la classe :class:`NavTarget`.

.. py:class:: NavTarget

   .. py:attribute:: id

      Chaîne de caractère, identifiant du ``<pageList>``.

   .. py:attribute:: labels
   
      Liste des labels du ``<navPoint>`` : chaque label et un tuple de la forme 
      ``(label, lang, dir)``, indiquant respectivement le titre du label, sa 
      langue, et la direction d'écriture (``ltr`` ou ``rtl``).

   .. py:attribute:: value
   
      Chaîne de caractères, représente l'attribut ``value`` de l'élément.

   .. py:attribute:: class_name
   
      Chaîne de caractère, indique la classe css proposée.
      
   .. py:attribute:: play_order
   
      Chaîne de caractère, indique le placement dans l'ordre de lecture de 
      l'élément. Peut être vide.
      
   .. py:attribute:: src
   
      Chaîne de caractère, indique l'url relative à l'emplacement du fichier 
      NCX, et pouvant pointer vers des fragments de fichiers du fichier epub.
      
      Exemple : ``Text/chap1.xhtml#p36`` indique le fichier 
      ``Text/chap1.xhtml`` et plus spéficiquement à l'emplacement du fragment 
      ``p36``.
