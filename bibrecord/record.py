"""
record module of the bibrecord package.
"""

import logging
import re

logger = logging.getLogger(__name__)


class Record:
    """
    Base class for each bibliography record.

    More description comes here...


    Attributes
    ----------
    attr : :class:`None`
        Short description

    Raises
    ------
    exception
        Short description when and why raised


    Examples
    --------
    It is always nice to give some examples how to use the class. Best to do
    that with code examples:

    .. code-block::

        obj = Record()
        ...

    

    """

    # noinspection PyMethodMayBeStatic
    def to_string(self):
        return ''

    def to_bib(self):
        items = []
        for prop in self._get_public_properties():
            items.append("\t{} = {{{}}}".format(prop, getattr(self, prop)))
        output = "@{}{{\n{}\n}}".format(__class__.__name__, ',\n'.join(items))
        return output

    def _get_public_properties(self):
        properties = []
        for prop in list(self.__dict__.keys()):
            if not str(prop).startswith('_'):
                properties.append(prop)
        return properties


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


    Examples
    --------
    It is always nice to give some examples how to use the class. Best to do
    that with code examples:

    .. code-block::

        obj = Person()
        ...

    """

    def __init__(self):
        self.first = ''
        self.last = ''
        self.particle = ''
        self.suffix = ''
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
        last = self.last
        if self.particle:
            last = '{} {}'.format(self.particle, self.last)
        if self.suffix:
            last = '{}, {}'.format(last, self.suffix)
        if self.reverse:
            output = '{}, {}'.format(last, self.first)
        else:
            output = '{} {}'.format(self.first, last)
        return output

    def to_bib(self):
        original_reverse_property = self.reverse
        if self.particle or self.suffix:
            self.reverse = True
        output = self.to_string()
        self.reverse = original_reverse_property
        return output
