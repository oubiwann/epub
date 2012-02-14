Documentation du module epub.opf
================================

.. py:module:: epub.opf

.. toctree::
   :maxdepth: 2

.. py:class:: Opf()

   Le format OPF permet de décrire le contenu d'un fichier epub : il décrit non 
   seulement les méta-données (titres, auteurs, etc.) mais aussi la liste des 
   fichiers qui représentent le contenu du livre.

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

.. py:class:: Manifest()

   Représente l'élément ``<manifest>`` d'un fichier OPF.

   Cet élément référence la liste des fichiers du livre numérique : textes, 
   images, feuilles de style, couverture, etc. ainsi que les _fallback_ des 
   fichiers qui sortent de la spécification Epub (comme les fichiers PDF).

.. py:class:: Metadata()

   Cette classe permet de représenter les meta-données décrites dans le fichier 
   OPF du fichier epub, contenu dans la balise ``<metadata>``. La description 
   de chacune de ces meta-données est disponible dans la `spécification Epub, 
   section "Metadata"`__.

   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.2

   Les règles suivantes s'appliquent à tous les attributs composés de plusieurs 
   éléments :

   * La valeur d'une meta-donnée est représentée par un tuple de ses attributs, 
     chacun représenté par une chaîne de caractère
   * Une meta-donnée peut être présente plusieurs fois avec des valeurs 
     différentes : chacune est alors stockée dans une liste
   * Un attribut qui n'est pas renseigné dans le fichier xml est représenté par 
     une chaîne vide.

   Ainsi, l'attribut :attr:`titles` est une ``list`` de ``tuple`` de la 
   forme ``(title, lang)``.

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

   L'élément ``<dc:coverage>``, représenté par une chaîne de caractère.

   .. py:attribute:: metas

   Liste des éléments ``<dc:meta>`` des meta-données. Chaque élément de la 
   liste est un tuple de la forme ``(name, content)``.

.. py:class:: Guide

   L'élément ``<guide>`` d'un fichier OPF représente une liste des tables et 
   des références du livre, pouvant indiquer la couverture, la table des 
   contenus, des illustrations, etc.
   
   Voir aussi la `spécification epub OPF, section "guide"`__
   
   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.6

.. py:class:: Spine

   Permet de représenter l'élément ``<spine>`` d'un fichier OPF.
   
   Cet élément indique une liste de fichiers dans un ordre de lecture dit 
   "linéaire", c'est à dire dans l'ordre de lecture logique.

   Voir aussi la `spécification epub OPF, section "spine"`__
   
   .. __: http://idpf.org/epub/20/spec/OPF_2.0.1_draft.htm#Section2.4
