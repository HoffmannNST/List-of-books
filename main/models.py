from django.db import models

# Create your models here.
class Books(models.Model):
    """Books model that holds title, author, publication_date,
    ISBN, page_count, front_page_link and language.

    Returns:
        str: all the held information
    """

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=30)
    page_count = models.IntegerField()
    front_page_link = models.URLField()
    language = models.CharField(max_length=40)

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}".format(
            self.title,
            self.author,
            self.publication_date,
            self.isbn,
            self.page_count,
            self.front_page_link,
            self.language,
        )
