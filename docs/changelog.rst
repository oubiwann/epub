Changelog
=========

.. toctree::
   :maxdepth: 2

Version 0.5.0
-------------

Encore de nouvelles améliorations.

* Ajout de la méthode :meth:`epub.EpubFile.check_mode_write` qui lève une
  exception si le fichier n'est pas ouvert en écriture.
* Support de python 2.6 avec l'emploi du module `ordereddict` disponible sur
  pypi (http://pypi.python.org/pypi/ordereddict) (il manque des tests pour
  être certain du bon fonctionnement avec Python 2.6).
* Nouvelle classe `epub.Book` servant de proxy pour simplifier et abstraire
  la manipulation du format epub. *Fonctionnalité expérimentale*.
* Ajout de la méthode :meth:`epub.EpubFile.extract_item` qui reprend le même
  principe que :meth:`~epub.EpubFile.read_item` en l'appliquant à l'exctraction
  de fichiers.
* Ajout de la fonction :func:`epub.utils.get_urlpath_part` permettant d'obtenir
  les deux parties des chemins des fichiers utilisés (entre autre) dans le
  fichier NCX ou l'élément spine du fichier OPF.
* Support de Python 3.2, avec des test-unitaires passant avec Python 2.7 et
  Python 3.2.
* Retrait de la notation des chaînes unicodes (le `u` devant les chaînes de
  caractères est retiré) dans la documentation.
* Ajout d'un warning sur l'usage de la fonction `epub.open()` : fonction
  dépréciée. Il vaut mieux utiliser :func:`epub.open_epub` à la place, qui
  prend les mêmes paramètres, mais évite tout potentiel conflit avec la
  fonction python `open()`.
* Ajout d'une note sur la version et la compatibilité avec les versions de 
  Python dans la documentation.

Bug fix
.......

Les bugs suivants ont été résolus :

* `Issue #2`__ : *"Documentation pub on tutorial page."*
  La documentation ne fait plus de références à la méthode `read` dans ses
  exemples.
* `Issue #3`__ : *"_parse_xml_metadata should not choke on absent firstChild"*
  Une fonction a été ajoutée pour traiter la récupération de texte dans un
  noeud xml, et cette fonction est suffisament intelligente pour ne pas
  planter au premier texte manquant. Voir aussi
  :func:`epub.utils.get_node_text`.

.. __: https://bitbucket.org/exirel/epub/issue/2/documentation-pub-on-tutorial-page
.. __: https://bitbucket.org/exirel/epub/issue/3/_parse_xml_metadata-should-not-choke-on


Version 0.4.0
-------------

Cette nouvelle version propose plusieurs petites améliorations, ainsi qu'une
nouvelle fonctionnalité majeure : le mode écriture.

L'API n'est plus tout à fait la même, notamment les méthodes pour lire les
fichiers ont changé un peu. Au vu des grands changements introduits par cette
version, elle **n'est pas compatible** avec les versions précédentes.

De plus, cette version n'est compatible qu'avec Python 2.7. Il est prévu de
supporter Python 2.6 dans une prochaine version.

* La fonction :func:`epub.open` accepte un second paramètre `mode` pour choisir
  d'ouvrir le fichier en lecture seule ou en écriture.
* La méthode :meth:`epub.EpubFile.read` devient :meth:`epub.EpubFile.read_item`.
  Cette méthode possède le même fonctionnement que l'ancienne, qui reprend sa
  fonctionnalité native de la classe `zipfile.ZipFile`.
* La classe :class:`epub.opf.Manifest` étend la classe 
  :class:`collection.OrderedDict` et plus la type `dict`. Ce changement n'est
  pas compatible avec une autre version que Python 2.7, mais un backport sera
  proposé prochainement.
* Correction de divers bug, notamment sur le chargement des méta-données.
* Une meilleure documentation du module :mod:`epub.opf` et :mod:`epub.ncx`.
* Une couverture à 100% des tests unitaires.
* Ajout de ce fichier de changelog.
