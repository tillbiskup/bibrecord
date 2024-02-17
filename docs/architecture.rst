============
Architecture
============

Each software has some kind of architecture, and this is the place to describe it in broad terms, to make it easier for developers to get around the code.


Core domain
===========

The idea of the bibrecord package is to handle bibliographic records within source code in a way that the information contained in this records can be operated upon. The prototypical use case scenario: you implement an algorithm described in a publication, and you would like to cite this publication in the code -- in a way that users of your implementation can have the reference printed in a report or else.

Hence, the core abstraction of the bibrecord package is the bibliographic record, in its abstract form implemented in the :class:`bibrecord.record.Record` class. The bibliographic record is modelled following closely the overall scheme defined by the BibTeX file format and bibliography tool. Therefore, a bibliographic record defined by :class:`bibrecord.record.Record` or one of its subclasses -- you will never use :class:`bibrecord.record.Record` directly, but always a concrete subclass, such as :class:`bibrecord.record.Article` -- can be output directly as BibTeX record or as formatted textual reference. Nevertheless, the primary focus of the :class:`bibrecord.record.Record` class is on containing the relevant information (metadata) of the bibliographic record, and *not* any connection to the BibTeX world.


Extension: collections of records
=================================

Individual bibliographic records are handled by the :class:`bibrecord.record.Record` class and its descendants, as described above. However, sometimes there is the need to deal with collections of bibliographic records. A prototypical use case would be a package containing data from different sources (*i.e.*, with different references) where for each individual dataset the appropriate reference should be provided. Furthermore, datasets and bibliographic records may have an *n* to *m* relationship. Hence, it seems unreasonable to manually add the same reference(s) over and over in the code.

The solution is obvious: a collection of records, *i.e.* a bibliographic database, where we can access individual records based on a unique key. This is what the class :class:`bibrecord.database.Database` provides us with. How we get the information contained in the individual bibliographic records into the database in the first place is a different matter and an unimportant detail for now.


Periphery: reading BibTeX files
===============================

Some connection to the BibTeX world comes to no surprise after all. Particularly in light of collections of datasets, there is a need for a code-independent storage of the actual information contained in the individual bibliographic records, and the BibTeX format is well-established and quite robust.

The :mod:`bibrecord.bibtex` module contains two abstractions for dealing with BibTeX files and records: Individual BibTeX entries are represented as :class:`bibrecord.bibtex.Entry`, and entire BibTeX bibliographies as read from a file as :class:`bibrecord.bibtex.Bibliography`. Normal users will not care about the :class:`bibrecord.bibtex.Entry` class, as this is merely a proxy between the :class:`bibrecord.bibtex.Bibliography` and the individual machine-actionable bibliographic records of :class:`bibrecord.record.Record` contained in a :class:`bibrecord.database.Database`.

