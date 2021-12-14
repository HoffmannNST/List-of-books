from django.test import TestCase
from .models import Books

# Create your tests here.
class BooksModelTestCase(TestCase):
    def setUp(self):
        self.book = Books(
            title="Le Petit Prince",
            author="Antoine de Saint-Exupry",
            publication_date="2013-08-19",
            isbn="9781492184034",
            page_count=58,
            front_page_link="http://books.google.pl/books?id=rf9OnwEACAAJ&dq=Le+petit+pr&hl=&cd=5&source=gbs_api",
            language="fr",
        )

    def test_books_creation(self):
        self.book.save()
        self.assertIsNotNone(self.book.id)
