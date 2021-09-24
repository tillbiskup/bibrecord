"""
Facilities for representing bibliographic records.

Bibliographic records form the basis of bibliographies and proper citations
of other people's work, particularly in humanities and science.
"""

import logging
import re

logger = logging.getLogger(__name__)


class Record:
    """
    Base class for each bibliographic record.

    Actual bibliographic records are represented by classes inheriting from
    this class. The types of bibliographic records follow those known from
    BibTeX.

    Attributes
    ----------
    format : :class:`str`
        Format string used create string representation of bibliographic record

        For details, see :meth:`to_string`

    key : :class:`str`
        BibTeX key used to refer to the record

    reverse : :class:`bool`
        Whether to reverse last and first name in output

        Default: False


    Examples
    --------
    For examples of how to use this class, have a look at the examples of
    the classes that inherit from this one and implement actual types of
    bibliographic records.

    """

    def __init__(self, key=''):
        self.key = key
        self.format = ''
        self.reverse = False
        self._exclude = ['reverse', 'key', 'format']

    def to_string(self):
        """
        Return string representation of a bibliographic record.

        The format of the resulting string is controlled by the property
        :attr:`format`. There, you can use all the public properties of the
        class that form part of the bibliographic record, such as "author",
        "title", and alike.

        The properties "author" and "editor" are treated specially, to ensure
        the names to be appropriately formatted.

        .. note::
            The aim of this method is currently in no way to allow for
            advanced formatting including conditionals, as possible with
            BibTeX styles. It only provides a rudimentary way of converting
            a bibliographic record into a string representation.

        Returns
        -------
        output : :class:`str`
            String representation of a bibliography record

        """
        output = self.format
        for prop in self._get_public_properties():
            value = getattr(self, prop)
            if prop in ['author', 'editor']:
                value = ', '.join([self._person_to_string(x) for x in value])
            output = output.replace(prop, value)
        return output

    def to_bib(self):
        """
        Return BibTeX representation of a bibliography record as string.

        The BibTeX representation generally looks as follows:

        .. code-block::

            @Record(<key>,
                <property1> = {<value1>},
                ...
                <propertyN> = {<valueN>}
            }

        As you can see from this example, the output is quite opinionated,
        although BibTeX as such would allow for some slightly different
        formatting as well. To highlight the most important aspects:

        * Values are surrounded by curly brackets, not quotation marks.

        * The type of record is capitalised.

        * Indentation is done using tabulators.

        The record type is identical to the actual class used. The
        properties "author" and "editor" are treated specially, to ensure
        the names to be appropriately formatted.


        Returns
        -------
        record : :class:`str`
            BibTeX representation of a bibliography record

        """
        items = []
        for prop in self._get_public_properties():
            if getattr(self, prop):
                value = getattr(self, prop)
                if prop in ['author', 'editor']:
                    value = ' AND '.join([self._person_to_string(x, bib=True)
                                          for x in value])
                items.append(f"\t{prop} = {{{value}}}")
        string_items = ',\n'.join(items)
        output = f"@{__class__.__name__}{{{self.key},\n{string_items}\n}}"
        return output

    def _get_public_properties(self):
        properties = []
        for prop in list(self.__dict__.keys()):
            if not str(prop).startswith('_') and prop not in self._exclude:
                properties.append(prop)
        return properties

    def _person_to_string(self, string, bib=False):
        person = Person()
        person.reverse = self.reverse
        person.from_bib(string)
        if bib:
            output = person.to_bib()
        else:
            output = person.to_string()
        return output


class Person:
    """
    Representation of a person's name.

    Names consist, according to BibTeX, of four parts: first (given names),
    last (family name), particle (*e.g.*, von), suffix (*e.g.*, Jr., III).


    Attributes
    ----------
    first : :class:`str`
        First or given name of a person

    last : :class:`str`
        Last or family name of a person

    particle : :class:`str`
        Particle such as "von", usually prefixing the last name

    suffix : :class:`str`
        Suffix of a person's last name, such as "Jr." or "III"

    reverse : :class:`bool`
        Whether to reverse last and first name in output

        Default: False


    Examples
    --------
    There are different usage scenarios for this class. The first is to
    populate the properties of an object from a (BibTeX) string:

    .. code-block::

        person = Person()
        person.from_bib('John Doe')

    This will result in the object ``person`` having set "John" as its
    property "first" and "Doe" as its property "last". Note that a person's
    name consists (according to BibTeX) of four parts. See :meth:`from_bib`
    for details.

    The other way round, you may want to have a string representation of a
    person's name, either in plain text representation or for use within a
    BibTeX record:

    .. code-block::

        string = person.to_string()
        bib_string = person.to_bib()

    The difference of these two methods is quite subtle, and only present if
    at least one of "particle" or "suffix" is present. In the latter case,
    :meth:`to_bib` will return a string that can be understood by BibTeX,
    *i.e.* with reversed order of names, meaning the first name output last
    and separated by a comma.

    """

    def __init__(self, first='', last='', particle='', suffix=''):
        self.first = first
        self.last = last
        self.particle = particle
        self.suffix = suffix
        self.reverse = False

    def from_bib(self, string):
        """
        Set properties of a person's name from a BibTeX record.

        There are quote some different ways one can format a person's name
        in a BibTeX record, and not all are (currently) supported. See below
        for a list of variants that are currently supported:

        * FIRST LAST
        * LAST, FIRST
        * PARTICLE LAST, FIRST
        * LAST, SUFFIX, FIRST
        * PARTICLE LAST, SUFFIX, FIRST

        For the meaning of FIRST, LAST, PARTICLE, and SUFFIX see the class
        documentation.

        Parameters
        ----------
        string : :class:`str`
            String containing person's name

        """
        # Reduce additional whitespace
        string = re.sub(r'\s{2,}', r' ', string.strip())
        parts = string.split(',')
        if len(parts) > 2:
            self.suffix = parts.pop(1).strip()
        if len(parts) > 1:
            self.first = parts[1].strip()
            last_parts = parts[0].strip().rsplit(' ', maxsplit=1)
            if len(last_parts) > 1:
                self.particle = last_parts.pop(0)
            self.last = last_parts[0]
        else:
            self.first, self.last = string.rsplit(' ', maxsplit=1)

    def to_string(self):
        """
        Return the string representation of a person's name.

        Depending on the property :attr:`reverse`, the name is returned with
        first name first or last. Some examples:

        * FIRST LAST
        * FIRST PARTICLE LAST
        * FIRST LAST, SUFFIX
        * FIRST PARTICLE LAST, SUFFIX

        Returns
        -------
        string : :class:`str`
            String representation of a person's name

        """
        last = self.last
        if self.particle:
            last = f'{self.particle} {self.last}'
        if self.suffix:
            last = f'{last}, {self.suffix}'
        if self.reverse:
            output = f'{last}, {self.first}'
        else:
            output = f'{self.first} {last}'
        return output

    def to_bib(self):
        """
        Return the BibTeX-compatible string representation of a person's name.

        The output is basically the same as for :meth:`to_string`, as long
        as neither particle nor suffix are set. If either of these is
        present, :attr:`reverse` is temporarily set to True.

        Returns
        -------
        string : :class:`str`
            BibTeX-compatible string representation of a person's name

        """
        original_reverse_property = self.reverse
        if self.particle or self.suffix:
            self.reverse = True
        output = self.to_string()
        self.reverse = original_reverse_property
        return output


class Article(Record):
    """
    Bibliographic record for an article published in a journal.

    Probably the primary way of publishing nowadays in science is to write
    an article and to submit this article to a journal for publication.

    The four essential properties of a bibliographic record of an article,
    according to BibTeX, are: :attr:`author`, :attr:`title`, :attr:`journal`,
    and :attr:`year`.

    Of course, to make sense of such a record, usually you would like to
    have at least :attr:`volume` and :attr:`pages` in addition to those
    properties.

    A purely optional, though sometimes very helpful property is the
    :attr:`doi`, *i.e.* the unique digital object identifier allowing you to
    retrieve the electronic version of this article if you happen to have
    access to the internet (and your institution subscribes to the
    publisher's content).


    Attributes
    ----------
    author : :class:`list`
        List of author names (as strings)

    title : :class:`str`
        Title of the article

    journal : :class:`str`
        Name of the journal the article appeared in

    year : :class:`str`
        Year the article was published

    volume : :class:`str`
        Volume of the journal the article appeared in

    pages : :class:`str`
        Range of pages (or article id)

    doi : :class:`str`
        Digital object identifier referring to the article


    Examples
    --------
    One use case (and the original reason for writing this package) is to
    specify a bibliographic record within another class, for example in case
    you've implemented an algorithm and want to give credit to the original
    authors in a somewhat portable way. As you can directly give the
    properties on object instantiation, this looks quite natural:

    .. code-block::

        reference = Article(
            author=['J. Timmer', 'M. König'],
            title="On generating power law noise",
            journal="Astronomy and Astrophysics",
            volume="300",
            pages="707--710",
            year="1995"
        )

    If you would want to output the above reference as a string, simply use
    the :meth:`to_string` method:

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

    If you would want to create a BibTeX record from this, make sure to
    first add a key:

    .. code-block::

        reference.key = 'timm-aaa-300-707'
        reference.to_bib()

    The output of ``print(reference.to_bib())`` would look as follows:

    .. code-block:: text

        @Record{timm-aaa-300-707,
            author = {J. Timmer AND M. König},
            title = {On generating power law noise},
            journal = {Astronomy and Astrophysics},
            year = {1995},
            volume = {300},
            pages = {707--710}
        }

    Thus, you can easily create a BibTeX bibliography from your bibliography
    records that should work well with BibTeX.

    """

    def __init__(self, key='', author=None, title='', journal='', year='',
                 volume='', pages='', doi=''):
        super().__init__(key=key)
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.pages = pages
        self.doi = doi
        self.format = 'author: title. journal volume:pages, year.'
