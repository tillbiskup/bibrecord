import unittest

from bibrecord import bibtex


ARTICLE = """
@Article{doe-foo-1-1,
    author = {John Doe},
    title = {Lorem ipsum},
    journal = {Foo},
    pages = {1--2},
    year = {2024}
}
"""

BOOK = """
@Book{doe-j-2024,
    author = {John Doe},
    title = {Lorem ipsum},
    publisher = {Foo},
    address = {Bar},
    year = {2024}
}
"""


class TestEntry(unittest.TestCase):
    def setUp(self):
        self.entry = bibtex.Entry()
        self.article_entry = ARTICLE
        self.book_entry = BOOK

    def test_instantiate_class(self):
        pass

    def test_from_bib_sets_record(self):
        self.entry.from_bib(self.article_entry)
        self.assertTrue(self.entry.record)
        self.assertEqual(self.article_entry, self.entry.record)

    def test_from_bib_with_article_sets_type(self):
        self.entry.from_bib(self.article_entry)
        self.assertTrue(self.entry.type)
        self.assertEqual("article", self.entry.type)

    def test_from_bib_with_book_sets_type(self):
        self.entry.from_bib(self.book_entry)
        self.assertTrue(self.entry.type)
        self.assertEqual("book", self.entry.type)

    def test_from_bib_sets_key(self):
        self.entry.from_bib(self.book_entry)
        self.assertTrue(self.entry.key)
        self.assertEqual("doe-j-2024", self.entry.key)

    def test_from_bib_sets_fields_dict(self):
        self.entry.from_bib(self.book_entry)
        self.assertTrue(self.entry.fields)
