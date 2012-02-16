Python-Epub
===========

.. toctree::
   :maxdepth: 2

   epub/index
   epub/opf
   epub/ncx

Introduction
------------

Connaissez-vous le format de livre numérique appelé "Epub" ? Il s'agit d'un 
format ouvert, proposé par l'`IDPF`_, qui le présente ainsi :

  EPUB is the distribution and interchange format standard for digital 
  publications and documents based on Web Standards. EPUB defines a means of 
  representing, packaging and encoding structured and semantically enhanced 
  Web content — including XHTML, CSS, SVG, images, and other resources — for 
  distribution in a single-file format.
  
  EPUB allows publishers to produce and send a single digital publication 
  file through distribution and offers consumers interoperability between 
  software/hardware for unencrypted reflowable digital books and other 
  publications.

En d'autre terme : c'est un format qui permet de rassembler dans un seul 
fichier un ensemble de fichiers de type "html&css", pour publier du contenu - 
du genre, un livre numérique.

Dans le monde python, si vous cherchez bien, vous trouverez des solutions tout 
à fait pertinentes d'applications pour lire et éditer des fichiers epub.

Cependant, il s'agit beaucoup de solutions spécifiques (et en outre, très peu 
de bibliothèques), d'où l'existence de cette bibliothèque qui permet d'ouvrir 
(en lecture seule pour le moment) des fichiers au format epub (dans la version 
2 de la spécification, pour le moment).

Voir aussi : le site l'`IDPF`_ et la `spécification Epub 2`_.

.. _IDPF: http://idpf.org/epub
.. _spécification Epub 2: http://idpf.org/epub/201

.. warning::

   Pour le moment, cette bibliothèque est en phase de développement. Chaque 
   release effectuée sur pypi est testée unitairement (ce qui évite en théorie 
   la présence de bugs), mais l'API n'est pas dans une forme stable. Des 
   changements et évolutions sont notamment à prévoir sur la façon d'accéder 
   aux fichiers contenus dans l'archive epub.
   
   En outre il est vivement déconseillé d'utiliser la version de développement 
   à partir du repository mercurial, ce derniers étant tout sauf stable. Vous 
   êtes par contre vivement encouragés à l'utiliser pour détecter des bugs, 
   proposer des améliorations, et/ou remonter toutes les incohérences et/ou 
   maladresses présentes dans le code.
   
   Les bonnes volontés et les remarques sont **toutes** bonnes à prendre.

Licence
-------

La licence choisie pour cette bibliothèque est la LGPL_.

.. _LGPL: http://www.gnu.org/licenses/lgpl.html

Installation
------------

Disponible sur pypi, vous pouvez installer Python Epub via la commande "pip" :

.. code-block:: bash

  pip install epub

Sinon, vous pouvez obtenir la dernière version des sources via mercurial :

.. code-block:: bash

  hg clone https://bitbucket.org/exirel/epub
  cd epub
  python setup.py install

Utilisation
-----------

Le cas d'utilisation le plus simple est représenté par le code suivant :

::

  import epub
  
  book = epub.open('path/to/my/book.epub')
  
  for item in book.opf.manifest.items:
      content = book.read(item)
      # do something very nice with the content

Bien entendu, ce n'est qu'un exemple, très incomplet qui plus est, de ce que 
vous pouvez faire.

Cette bibliothèque ayant pour ambition de suivre les spécifications du format 
epub, certains éléments pourront paraître obscurs.

Rassurez-vous, cette documentation est là pour vous apporter le plus possible 
de réponses à vos interrogations.


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

