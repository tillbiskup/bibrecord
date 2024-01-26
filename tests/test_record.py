import unittest

from bibrecord import record


class TestRecord(unittest.TestCase):

    def setUp(self):
        self.record = record.Record()

    def test_instantiate_class(self):
        pass

    def test_key_property_can_be_set_by_instantiation(self):
        record_ = record.Record(key="foo")
        self.assertEqual("foo", record_.key)

    def test_has_to_string_method(self):
        self.assertTrue(hasattr(self.record, "to_string"))
        self.assertTrue(callable(self.record.to_string))

    def test_to_string_returns_string(self):
        self.assertTrue(isinstance(self.record.to_string(), str))

    def test_to_string_with_format_and_properties_returns_string(self):
        self.record.format = "author: title"
        self.record.author = ["John Doe"]
        self.record.title = "Lorem ipsum"
        output = f"{self.record.author[0]}: {self.record.title}"
        self.assertEqual(output, self.record.to_string())

    def test_to_string_with_format_and_authors_returns_string(self):
        self.record.format = "author: title"
        self.record.author = ["John Doe", "Max Mustermann"]
        self.record.title = "Lorem ipsum"
        authors = ", ".join(self.record.author)
        output = f"{authors}: {self.record.title}"
        self.assertEqual(output, self.record.to_string())

    def test_to_string_with_format_and_author_with_suffix_returns_string(
        self,
    ):
        self.record.format = "author: title"
        self.record.author = ["Doe, Jr., John"]
        self.record.title = "Lorem ipsum"
        output = f"John Doe, Jr.: {self.record.title}"
        self.assertEqual(output, self.record.to_string())

    def test_to_string_with_format_and_author_and_reverse_returns_string(
        self,
    ):
        self.record.format = "author: title"
        self.record.author = ["John Doe"]
        self.record.title = "Lorem ipsum"
        self.record.reverse = True
        output = f"Doe, John: {self.record.title}"
        self.assertEqual(output, self.record.to_string())

    def test_has_to_bib_method(self):
        self.assertTrue(hasattr(self.record, "to_bib"))
        self.assertTrue(callable(self.record.to_bib))

    def test_to_bib_returns_string(self):
        self.assertTrue(isinstance(self.record.to_string(), str))

    def test_to_bib_returns_bibtex_record(self):
        output = "@Record{,\n\n}"
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_key_returns_bibtex_record_with_key(self):
        output = "@Record{foo,\n\n}"
        self.record.key = "foo"
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_property_adds_property_to_bibtex_record(self):
        self.record.author = ["John Doe"]
        output = "@Record{,\n\tauthor = {John Doe}\n}"
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_empty_property_returns_empty_bibtex_record(self):
        output = "@Record{,\n\n}"
        self.record.title = ""
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_properties_adds_properties_to_bibtex_record(self):
        self.record.author = ["John Doe"]
        self.record.title = "Lorem ipsum"
        output = (
            "@Record{,\n\tauthor = {John Doe},\n\ttitle = {Lorem ipsum}\n}"
        )
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_author_reversed_adds_author_to_bibtex_record(self):
        self.record.author = ["John Doe"]
        self.record.reverse = True
        output = "@Record{,\n\tauthor = {Doe, John}\n}"
        self.assertEqual(self.record.to_bib(), output)

    def test_to_bib_with_authors_adds_authors_to_bibtex_record(self):
        self.record.author = ["John Doe", "Max Mustermann"]
        output = "@Record{,\n\tauthor = {John Doe AND Max Mustermann}\n}"
        self.assertEqual(self.record.to_bib(), output)


class TestPerson(unittest.TestCase):

    def setUp(self):
        self.person = record.Person()
        self.first = "John"
        self.last = "Doe"
        self.particle = "van der"
        self.suffix = "Jr."

    def test_instantiate_class(self):
        pass

    def test_has_properties(self):
        for prop in ["first", "last", "particle", "suffix"]:
            self.assertTrue(hasattr(self.person, prop))

    def test_has_from_bib_method(self):
        self.assertTrue(hasattr(self.person, "from_bib"))
        self.assertTrue(callable(self.person.from_bib))

    def test_from_bib_sets_first_and_last(self):
        self.person.from_bib("{} {}".format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_additional_spaces_sets_first_and_last(self):
        self.person.from_bib("{}   {}".format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_leading_spaces_sets_first_and_last(self):
        self.person.from_bib("  {} {}".format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_trailing_spaces_sets_first_and_last(self):
        self.person.from_bib("{} {}  ".format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_to_first_names_sets_first_and_last(self):
        self.first = "John R."
        self.person.from_bib("{} {}".format(self.first, self.last))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_names_reversed_sets_first_and_last(self):
        self.person.from_bib("{}, {}".format(self.last, self.first))
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)

    def test_from_bib_with_particle_sets_particle(self):
        self.person.from_bib(
            "{} {}, {}".format(self.particle, self.last, self.first)
        )
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)
        self.assertEqual(self.particle, self.person.particle)

    def test_from_bib_with_suffix_sets_particle(self):
        self.person.from_bib(
            "{} {}, {}, {}".format(
                self.particle, self.last, self.suffix, self.first
            )
        )
        self.assertEqual(self.first, self.person.first)
        self.assertEqual(self.last, self.person.last)
        self.assertEqual(self.particle, self.person.particle)
        self.assertEqual(self.suffix, self.person.suffix)

    def test_has_to_string_method(self):
        self.assertTrue(hasattr(self.person, "to_string"))
        self.assertTrue(callable(self.person.to_string))

    def test_to_string_returns_string(self):
        self.assertTrue(isinstance(self.person.to_string(), str))

    def test_to_string_with_first_and_last(self):
        string = "{} {}".format(self.first, self.last)
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle(self):
        string = "{} {} {}".format(self.first, self.particle, self.last)
        bib_string = "{} {}, {}".format(self.particle, self.last, self.first)
        self.person.from_bib(bib_string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_suffix(self):
        string = "{} {}, {}".format(self.first, self.last, self.suffix)
        bib_string = "{}, {}, {}".format(self.last, self.suffix, self.first)
        self.person.from_bib(bib_string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle_and_suffix(self):
        string = "{} {} {}, {}".format(
            self.first, self.particle, self.last, self.suffix
        )
        bib_string = "{} {}, {}, {}".format(
            self.particle, self.last, self.suffix, self.first
        )
        self.person.from_bib(bib_string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_first_and_last_reversed(self):
        string = "{}, {}".format(self.last, self.first)
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle_reversed(self):
        string = "{} {}, {}".format(self.particle, self.last, self.first)
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_suffix_reversed(self):
        string = "{}, {}, {}".format(self.last, self.suffix, self.first)
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_to_string_with_particle_and_suffix_reversed(self):
        string = "{} {}, {}, {}".format(
            self.particle, self.last, self.suffix, self.first
        )
        self.person.reverse = True
        self.person.from_bib(string)
        output = self.person.to_string()
        self.assertEqual(string, output)

    def test_has_to_bib_method(self):
        self.assertTrue(hasattr(self.person, "to_bib"))
        self.assertTrue(callable(self.person.to_bib))

    def test_to_bib_returns_string(self):
        self.assertTrue(isinstance(self.person.to_bib(), str))

    def test_to_bib_with_particle_returns_reversed(self):
        string = "{} {}, {}".format(self.particle, self.last, self.first)
        self.person.reverse = False
        self.person.from_bib(string)
        output = self.person.to_bib()
        self.assertEqual(string, output)

    def test_to_bib_with_suffix_returns_reversed(self):
        string = "{}, {}, {}".format(self.last, self.suffix, self.first)
        self.person.reverse = False
        self.person.from_bib(string)
        output = self.person.to_bib()
        self.assertEqual(string, output)

    def test_to_bib_with_particle_resets_reverse_property(self):
        string = "{} {}, {}".format(self.particle, self.last, self.first)
        self.person.reverse = False
        self.person.from_bib(string)
        self.person.to_bib()
        self.assertFalse(self.person.reverse)


class TestArticle(unittest.TestCase):

    def setUp(self):
        self.article = record.Article()
        self.author = ["John Doe"]
        self.title = "Lorem ipsum"
        self.journal = "J. Peculiar Res."
        self.volume = "42"
        self.pages = "0"
        self.year = "1968"

    def test_instantiate_class(self):
        pass

    def test_has_properties(self):
        for prop in [
            "author",
            "title",
            "journal",
            "year",
            "volume",
            "pages",
            "doi",
        ]:
            self.assertTrue(hasattr(self.article, prop))

    def test_properties_can_be_set_by_instantiation(self):
        article = record.Article(author=self.author)
        self.assertEqual(self.author, article.author)

    def test_has_sensible_default_format(self):
        article = record.Article(
            author=self.author,
            title=self.title,
            journal=self.journal,
            volume=self.volume,
            pages=self.pages,
            year=self.year,
        )
        authors = ", ".join(self.author)
        output = (
            f"{authors}: {self.title}. {self.journal} {self.volume}:"
            f"{self.pages}, {self.year}."
        )
        self.assertEqual(output, article.to_string())

    def test_to_bib_returns_bibtex_record_with_correct_type(self):
        output = "@Article{,\n\n}"
        self.assertEqual(self.article.to_bib(), output)


class TestBook(unittest.TestCase):

    def setUp(self):
        self.book = record.Book()
        self.author = ["John Doe"]
        self.title = "Lorem ipsum"
        self.publisher = "Springer"
        self.year = "1968"
        self.address = "Berlin"
        self.edition = "1"

    def test_instantiate_class(self):
        pass

    def test_has_properties(self):
        for prop in [
            "author",
            "editor",
            "title",
            "publisher",
            "year",
            "address",
            "edition",
        ]:
            self.assertTrue(hasattr(self.book, prop))

    def test_properties_can_be_set_by_instantiation(self):
        book = record.Book(author=self.author)
        self.assertEqual(self.author, book.author)

    def test_has_sensible_default_format(self):
        book = record.Book(
            author=self.author,
            title=self.title,
            publisher=self.publisher,
            year=self.year,
            address=self.address,
        )
        authors = ", ".join(self.author)
        output = (
            f"{authors}: {self.title}. {self.publisher}, {self.address} "
            f"{self.year}."
        )
        self.assertEqual(output, book.to_string())

    def test_with_editor_has_sensible_default_format(self):
        book = record.Book(
            editor=self.author,
            title=self.title,
            publisher=self.publisher,
            year=self.year,
            address=self.address,
        )
        editors = ", ".join(self.author)
        output = (
            f"{editors} (Ed.): {self.title}. {self.publisher},"
            f" {self.address} "
            f"{self.year}."
        )
        self.assertEqual(output, book.to_string())

    def test_to_bib_returns_bibtex_record_with_correct_type(self):
        output = "@Book{,\n\n}"
        self.assertEqual(self.book.to_bib(), output)
