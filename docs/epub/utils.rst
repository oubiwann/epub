Utilitaires
===========

.. py:module:: epub.utils

.. toctree::
   :maxdepth: 2

Pour des raisons pratiques, le module :mod:`epub` propose un module utilitaire
appelé :mod:`epub.utils`. Il regroupe les fonctions pratiques à utilisées.


.. py:function:: get_node_text(node)

   Retourne le contenu texte d'un noeud XML de type `ELEMENT_NODE`. Si le texte
   est vide (le tag est vide), la valeur de retour sera une chaîne vide.

   :param node: Le noeud XML dont on cherche à récupérer le texte.
   :ptype node: :class:`xml.dom.Element`
   :rtype: string

.. py:function:: get_urlpath_part(url)

   Découpe une url en deux parties : l'url sans fragment, et le fragment.
   S'il n'y a pas de fragment alors l'url est retournée telle qu'elle avec
   fragment à `None`.

   .. code-block:: python

      url = 'text/chapter1.xhtml#part2'
      href, fragment = get_urlpath_part(url)
      print href # 'text/chapter1.xhtml'
      print fragment # '#part2'

   :param string url: Le chemin d'un fichier à décomposer en deux parties.
   :rtype: tuple