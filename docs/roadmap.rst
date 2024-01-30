=======
Roadmap
=======

A few ideas how to develop the project further, currently a list as a reminder for the main developers themselves, in no particular order, though with a tendency to list more important aspects first:


For version 0.2
===============

* Class ``Bibliography`` or ``Database`` in :mod:`bibrecord.bibtex` module for reading and parsing BibTeX database files.
* Module ``bibliography`` or ``databaase`` with class ``Database`` reading BibTeX bibliography files (via ``bibrecord.bibtex.Bibliography``) and creating record objects.


For later versions
==================

* Remaining standard BibTeX record types

* Adding all optional properties for record types?

* Explicitly support biblatex-defined record types?

  `<https://mirrors.ctan.org/macros/latex/contrib/biblatex/doc/biblatex.pdf>`_

* Handling of "and" in lists of names? (Caution: internationalisation?)

* Template engine for string output formats
