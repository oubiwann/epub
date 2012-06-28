Changelog
=========

.. toctree::
   :maxdepth: 2

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
