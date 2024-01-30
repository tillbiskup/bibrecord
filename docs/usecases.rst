.. _use_cases:

=========
Use cases
=========

.. sidebar:: Contents

    .. contents::
        :local:
        :depth: 1


One use case (and the original reason for writing this package) is to
**specify a bibliographic record within another class**, for example in case
you've implemented an algorithm and want to give credit to the original
authors in a somewhat portable way.

Based on this idea, you may want to **output the information** contained in the bibliographic record in different ways, be it as some kind of string representation or as full-fledged BibTeX record for using it, *e.g.*, with the TeX/LaTeX typesetting system.


Bibliographic record within code
================================

The primary use case and original reason for writing this package is to
specify a bibliographic record within another class. Suppose you've implemented an algorithm for power law noise and want to give credit to the original authors within your code. As you can directly give the
properties on object instantiation, this looks quite natural:

.. code-block::

    reference = bibrecord.record.Article(
        author=['J. Timmer', 'M. König'],
        title="On generating power law noise",
        journal="Astronomy and Astrophysics",
        volume="300",
        pages="707--710",
        year="1995"
    )


In a more complete setting, showing a bit more code surrounding your class, this may look like:

.. code-block::

    import bibrecord


    class PowerLawNoise():

        def __init__(self):
            # ... your other properties go here
            self.reference = bibrecord.record.Article(
                author=['J. Timmer', 'M. König'],
                title="On generating power law noise",
                journal="Astronomy and Astrophysics",
                volume="300",
                pages="707--710",
                year="1995"
            )

So what's the advantage of this way of defining the relevant reference(s)? First of all, you define the reference in a structured fashion, making it quite easy to use the information contained in different ways (more of this below). Second, if you're somewhat familiar with BibTeX and its way of storing bibliographic records, this way of specifying the reference will feel quite familiar.

Why would you want to use this information of the bibliographic record? Suppose you have implemented some kind of report generation mechanism (perhaps even using a template engine) that summarises what has been done in a user-friendly and well-formatted way. Here, you probably want to include the relevant literature for specific algorithms as well. This can be done quite easily, as you don't need to parse your bibliographic record that you've buried somewhere as a string.


Output as string
================

As it has been mentioned above already, you may have ample of use cases where you want to output a reference as a string, *e.g.* in context of generating a report. To create a string representation of a bibliographic record, simply use its :meth:`to_string` method:

.. code-block::

    reference.to_string()

With the default format, this would result in the following text:

.. code-block:: text

    J. Timmer, M. König: On generating power law noise. Astronomy and
    Astrophysics 300:707--710, 1995.

Note that the line break is a matter of display here and not contained
in the original string output. Of course, if you would like to revert
the names, *i.e.* having the first name printed last, this can be done
as well:

.. code-block::

    reference.reverse = True
    reference.to_string()

With the default format, this would result in the following text:

.. code-block:: text

    Timmer, J., König, M.: On generating power law noise. Astronomy and
    Astrophysics 300:707--710, 1995.


Of course, there are nearly as many different citation styles as there are journals (and people). Therefore, the bibrecord package provides you with a simple yet quite powerful mechanism of formatting the string representation of your bibliographic records. Each record type has a ``format`` property. (For details, see :attr:`bibrecord.record.Record.format`). Here, you can define how you would want your string representation to look like.

.. note::

    At least for now, no complicated conditionals (as used in BibTeX styles) can be used when defining the format, as this would require using a template engine and contradict the approach of the bibrecord package to be as light-weight and simple to use as possible.


Create a BibTeX record
======================

The classes used for the different types of bibliographic records, such as article and book, clearly resemble the record types of BibTeX. Hence, you may want to create a BibTeX record from a record. This is pretty simple. Just make sure to first add a key:

.. code-block::

    reference.key = 'timm-aaa-300-707'
    reference.to_bib()

The output of ``print(reference.to_bib())`` would look as follows (for the reference defined above):

.. code-block:: text

    @Article{timm-aaa-300-707,
        author = {J. Timmer AND M. König},
        title = {On generating power law noise},
        journal = {Astronomy and Astrophysics},
        year = {1995},
        volume = {300},
        pages = {707--710}
    }

Thus, you can easily create a BibTeX bibliography from your bibliography
records that should work well with BibTeX.

.. note::

    As you can see, the bibrecord package is quite opinionated with respect to how a BibTeX record should look like. It uses curly brackets as delimiters for the fields of each key, not quotation marks, and capitalises the record type. Furthermore, unicode characters are directly output, hence it is your sole responsibility to use a BibTeX backend capable of dealing with unicode.


Handling multiple bibliographic records
=======================================

If you "only" want to have a bibliographic record as an attribute in a class,
say for an implementation of an algorithm where you would like to give credit
to the people who originally described the algorithm, one of the subclasses of
:class:`bibrecord.record.Record` is what you usually are interested in.

However, suppose you write a package that contains data from different sources
(*i.e.*, with different references) and you want to provide these references for
each individual dataset. In this case, you will probably have a BibTeX
bibliography file somewhere in the package data of your package that would be
the original source of the bibliographic information. In this case, being able
to convert this BibTeX bibliography file into an actionable representation for
your package would come quite handy. This is what the :class:`Database` class
provides you with.

Creating such a database is a matter of only a few lines. Suppose your BibTeX
database to reside in the file "literature.bib":

.. code-block::

    import bibrecord

    bibliography = bibrecord.bibtex.Bibliography()
    bibliography.from_file("literature.bib")
    database = bibrecord.database.Database()
    database.from_bibliography(bibliography)

Now you can access all bibliographic records from your :obj:`Database` object.

Assuming your database to contain the record used above several times, and having the associated BibTeX key ``timm-aaa-300-707``, adding this reference to a class in your code would simply become:

.. code-block::


    import bibrecord


    bibliography = bibrecord.bibtex.Bibliography()
    bibliography.from_file("literature.bib")
    database = bibrecord.database.Database()
    database.from_bibliography(bibliography)


    class PowerLawNoise():

        def __init__(self):
            # ... your other properties go here
            self.reference = database.records["timm-aaa-300-707"]


Of course, if you need to access one bibliographic database in your entire code base in multiple modules, it might be sensible to create the ``database`` object on the top level of your package, *e.g.* in the ``__init__.py`` file, so that you can import it from everywhere. This is close to a singleton object in a sense.
