import unittest

from bibrecord import record


class TestRecord(unittest.TestCase):

    def setUp(self):
        self.record = record.Record()

    def test_instantiate_class(self):
        pass

    def test_has_to_string_method(self):
        self.assertTrue(hasattr(self.record, 'to_string'))
        self.assertTrue(callable(self.record.to_string))

    def test_to_string_returns_string(self):
        self.assertTrue(isinstance(self.record.to_string(), str))

    def test_has_to_bib_method(self):
        self.assertTrue(hasattr(self.record, 'to_bib'))
        self.assertTrue(callable(self.record.to_bib))

    def test_to_bib_returns_string(self):
        self.assertTrue(isinstance(self.record.to_string(), str))

    def test_to_bib_returns_bibtex_record(self):
        output = "@Record{\n\n}"
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_property_adds_property_to_bibtex_record(self):
        self.record.author = 'John Doe'
        output = "@Record{\n\tauthor = {John Doe}\n}"
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_properties_adds_properties_to_bibtex_record(self):
        self.record.author = 'John Doe'
        self.record.title = 'Lorem ipsum'
        output = "@Record{\n\tauthor = {John Doe},\n\ttitle = {Lorem ipsum}\n}"
        self.assertEqual(self.record.to_bib(), output)


class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = record.Person()
        self.first = 'John'
        self.last = 'Doe'
        self.particle = 'van der'
        self.suffix = 'Jr.'

    def test_instantiate_class(self):
        pass

    def test_has_properties(self):
        for prop in ['first', 'last', 'particle', 'suffix']:
            self.assertTrue(hasattr(self.person, prop))

    def test_has_from_bib_method(self):
        self.assertTrue(hasattr(self.person, 'from_bib'))
        self.assertTrue(callable(self.person.from_bib))

    def test_from_bib_sets_first_and_last(self):
        self.person.from_bib('{} {}'.format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_additional_spaces_sets_first_and_last(self):
        self.person.from_bib('{}   {}'.format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_leading_spaces_sets_first_and_last(self):
        self.person.from_bib('  {} {}'.format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_trailing_spaces_sets_first_and_last(self):
        self.person.from_bib('{} {}  '.format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_to_first_names_sets_first_and_last(self):
        self.first = 'John R.'
        self.person.from_bib('{} {}'.format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_names_reversed_sets_first_and_last(self):
        self.person.from_bib('{}, {}'.format(self.last, self.first))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_particle_sets_particle(self):
        self.person.from_bib('{} {}, {}'.format(self.particle, self.last,
                                                self.first))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)
        self.assertEqual(self.particle, self.person.particle)

    def test_from_bib_with_suffix_sets_particle(self):
        self.person.from_bib('{} {}, {}, {}'.format(self.particle, self.last,
                                                    self.suffix, self.first))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)
        self.assertEqual(self.particle, self.person.particle)
        self.assertEqual(self.suffix, self.person.suffix)

    def test_has_to_string_method(self):
        self.assertTrue(hasattr(self.person, 'to_string'))
        self.assertTrue(callable(self.person.to_string))

    def test_to_string_returns_string(self):
        self.assertTrue(isinstance(self.person.to_string(), str))

    def test_to_string_with_first_and_last(self):
        string = '{} {}'.format(self.first, self.last)
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle(self):
        string = '{} {} {}'.format(self.first, self.particle, self.last)
        bib_string = '{} {}, {}'.format(self.particle, self.last, self.first)
        self.person.from_bib(bib_string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_suffix(self):
        string = '{} {}, {}'.format(self.first, self.last, self.suffix)
        bib_string = '{}, {}, {}'.format(self.last, self.suffix, self.first)
        self.person.from_bib(bib_string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle_and_suffix(self):
        string = '{} {} {}, {}'.format(self.first, self.particle, self.last,
                                       self.suffix)
        bib_string = '{} {}, {}, {}'.format(self.particle, self.last,
                                            self.suffix, self.first)
        self.person.from_bib(bib_string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_first_and_last_reversed(self):
        string = '{}, {}'.format(self.last, self.first)
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle_reversed(self):
        string = '{} {}, {}'.format(self.particle, self.last, self.first)
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_suffix_reversed(self):
        string = '{}, {}, {}'.format(self.last, self.suffix, self.first)
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle_and_suffix_reversed(self):
        string = '{} {}, {}, {}'.format(self.particle, self.last,
                                        self.suffix, self.first)
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_has_to_bib_method(self):
        self.assertTrue(hasattr(self.person, 'to_bib'))
        self.assertTrue(callable(self.person.to_bib))

    def test_to_bib_returns_string(self):
        self.assertTrue(isinstance(self.person.to_bib(), str))

    def test_to_bib_with_particle_returns_reversed(self):
        string = '{} {}, {}'.format(self.particle, self.last, self.first)
        self.person.reverse = False
        self.person.from_bib(string)
        output = self.person.to_bib()
        self.assertEqual(string, output)

    def test_to_bib_with_suffix_returns_reversed(self):
        string = '{}, {}, {}'.format(self.last, self.suffix, self.first)
        self.person.reverse = False
        self.person.from_bib(string)
        output = self.person.to_bib()
        self.assertEqual(string, output)

    def test_to_bib_with_particle_resets_reverse_property(self):
        string = '{} {}, {}'.format(self.particle, self.last, self.first)
        self.person.reverse = False
        self.person.from_bib(string)
        output = self.person.to_bib()
        self.assertFalse(self.person.reverse)
