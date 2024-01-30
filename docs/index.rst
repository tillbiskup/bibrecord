=======================
bibrecord documentation
=======================

*Handling bibliographic records within source code.*

Did you ever feel the need of **adding literature references to your (Python) code**, *e.g.* to an article describing the algorithm you just (re)implemented? Did you ever think: "Wouldn't it be useful to automatically output this reference in a generated report or else?" Are you somewhat familiar with how bibliographic records look like, *e.g.* from using BibTeX in conjunction with the TeX/LaTeX typesetting system? Then bibrecord may be the tool of choice for you.

Suppose you have implemented power-law noise and want to refer to the literature to give credit to those guys whose algorithm you've implemented. In this case, you could add the following record as an attribute to your class:

.. code-block::

    reference = bibrecord.record.Article(
        author=['J. Timmer', 'M. König'],
        title="On generating power law noise",
        journal="Astronomy and Astrophysics",
        volume="300",
        pages="707--710",
        year="1995"
    )

If you would like to output the reference as plain text, this would be as simple as:

.. code-block::

    reference.to_string()

The result:

J. Timmer, M. König: On generating power law noise. Astronomy and Astrophysics 300:707--710, 1995.

For everything else, have a look at the :doc:`use cases section <usecases>` or jump straight into the :doc:`API documentation <api/index>`. If you're unsure whether this package is something for you, you may as well read about :doc:`who is the target audience <audience>`.


Features
========

A list of features:

* Support for (a growing list of) different types of bibliographic records (articles, books).

* Straight-forward definition of bibliographic records, similar to BibTeX.

* Easy integration of a bibliographic record into your existing code base.

* Simple, yet powerful ways of creating a string representation or a BibTeX record from each bibliographic record.


And to make it even more convenient for users and future-proof:

* Open source project written in Python (>= 3.7)

* Pure Python, no external libraries/packages required

* Developed fully test-driven

* Extensive user and API documentation


Installation
============

To install the bibrecord package on your computer (sensibly within a Python virtual environment), open a terminal (activate your virtual environment), and type in the following:

.. code-block:: bash

    pip install bibrecord

For more details, see the :doc:`installation instructions <installing>`.


License
=======

This program is free software: you can redistribute it and/or modify it under the terms of the **BSD License**.



.. toctree::
   :maxdepth: 2
   :caption: User Manual:
   :hidden:

   audience
   usecases
   installing

.. toctree::
   :maxdepth: 2
   :caption: Developers:
   :hidden:

   people
   developers
   changelog
   roadmap
   api/index

