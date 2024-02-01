=========
Changelog
=========

This page contains a summary of changes between the official bibrecord releases. Only the biggest changes are listed here. A complete and detailed log of all changes is available through the `GitHub Repository Browser <https://github.com/tillbiskup/bibrecord>`_.


Version 0.2.0
=============

Released 2024-02-01


New features
------------

* New bibliographic record type for datasets: :class:`bibrecord.record.Dataset`.
* Read/populate records from BibTeX entries: :meth:`bibrecord.record.Record.from_bib`.
* Handling multiple bibliographic records: module :mod:`bibrecord.database` and class :class:`bibrecord.database.Database`.
* Basic handling of BibTeX bibliography files: module :mod:`bibrecord.bibtex`.


Documentation
-------------

* Description of the :doc:`overall architecture <architecture>` of the package.


Code quality
------------

* Automated code formatting using Black.


Version 0.1.0
=============

Released 2021-09-24

* First public release

* Support for article and book bibliographic record types

