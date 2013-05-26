#######################
EPub Library for Python
#######################

This project merges two efforts:

* Exirel's `epub`_.

* `timtanbin`_'s original python-epub-builder as well as `JohannesBuchner`_'s
  fork.

The revision histories for all three sources are preservied in git.

In all honesty, both project seem to be a bit of a mess; I'm just trying to
put something together that suites my needs. This code needs a *lot* of work.

Downloading
===========

You can use ``pip`` to install the Epub library:

.. code:: bash

    $ pip install https://github.com/oubiwann/epub/archive/master.zip

Or, you could clone the git repo:

.. code:: bash

    $ git clone https://github.com/oubiwann/epub.git
    $ cd epub
    $ python setup.py install


Documentation
=============

EPub Reader
-----------

.. code:: python

    from epub.reader import content

    mybook = content.open_epub('path/to/my/book.epub')

    for item in mybook.opf.manifest.values():
        # read the content
        data = mybook.read_item(item)


EPub Writer
-----------

.. code:: python

    from epub.writer import book

    (more soon ...)


.. Links
.. =====

.. _epub: https://bitbucket.org/exirel/epub
.. _timtanbin: http://code.google.com/p/python-epub-builder/
.. _JohannesBuchner: https://github.com/JohannesBuchner/python-epub-builder