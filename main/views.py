import requests
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import BookHandler, ImportBooks
from .models import Books
from .filters import BooksFilter
from .serializers import BooksSerializer

# Create your views here.


def list_of_books(request):
    books_list = Books.objects.order_by("title").all()

    my_filter = BooksFilter(request.GET, queryset=books_list)
    books_list = my_filter.qs

    context = {"list": books_list, "my_filter": my_filter}
    return render(request, "main/list_of_books.html", context)


def edit(request, item_id):
    if request.method == "POST":
        form = BookHandler(request.POST)
        if form.is_valid():
            title_var = form.cleaned_data["title"]
            author_var = form.cleaned_data["author"]
            publication_date_var = form.cleaned_data["publication_date"]
            isbn_var = form.cleaned_data["isbn"]
            page_count_var = form.cleaned_data["page_count"]
            front_page_link_var = form.cleaned_data["front_page_link"]
            language_var = form.cleaned_data["language"]

            if request.POST.get("create_new"):
                book = Books(
                    title=title_var,
                    author=author_var,
                    publication_date=publication_date_var,
                    isbn=isbn_var,
                    page_count=page_count_var,
                    front_page_link=front_page_link_var,
                    language=language_var,
                )
                book.save()
                messages.success(request, "Pomyślnie dodano nową książkę!")

            elif request.POST.get("change_book"):
                book = Books(
                    id=item_id,
                    title=title_var,
                    author=author_var,
                    publication_date=publication_date_var,
                    isbn=isbn_var,
                    page_count=page_count_var,
                    front_page_link=front_page_link_var,
                    language=language_var,
                )
                book.save()
                messages.success(request, "Pomyślnie edytowano książkę!")

            elif request.POST.get("delete_book"):
                book = Books.objects.get(id=item_id)
                book.delete()
                messages.success(request, "Pomyślnie usunięto książkę!")
                item_id = 0

            return HttpResponseRedirect("/edit/{}/".format(item_id))  # valid

        for errors in form.errors.values():  # validation error messages
            for error in errors:
                if error == "au_short":
                    messages.error(request, "Imię i nazwisko autora są zbyt krótkie!")
                elif error == "pc_small":
                    messages.error(request, "Liczba stron jest zbyt mała!")
        return HttpResponseRedirect("/edit/{}/".format(item_id))  # not valid

    else:
        if item_id == 0:
            form = BookHandler()
        else:
            book = Books.objects.get(id=item_id)
            form = BookHandler(
                initial={
                    "title": book.title,
                    "author": book.author,
                    "publication_date": book.publication_date,
                    "isbn": book.isbn,
                    "page_count": book.page_count,
                    "front_page_link": book.front_page_link,
                    "language": book.language,
                }
            )
        return render(request, "main/edit.html", {"form": form, "item_id": item_id})


def import_books(request):
    if request.method == "GET":
        form = ImportBooks(request.GET)
        if form.is_valid():  # if search form is valid search for books
            import_key_words = form.cleaned_data["import_key_words"]
            params = {"q": import_key_words}
            volumes_link = "https://www.googleapis.com/books/v1/volumes"
            api_request = requests.get(volumes_link, params)
            books_list = api_request.json()["items"]  # list with all info from api
            books_list_cleaned = []  # list for needed info only

            for item in books_list:  # get needed info only
                title = item["volumeInfo"]["title"]
                try:
                    author = item["volumeInfo"]["authors"]
                except KeyError:
                    author = ["Nie podano"]
                author = ", ".join(author)
                publication_date = item["volumeInfo"]["publishedDate"]
                if len(publication_date) == 4:
                    publication_date += "-01-01"
                elif len(publication_date) == 7:
                    publication_date += "-01"
                try:
                    isbn = item["volumeInfo"]["industryIdentifiers"][-1]["identifier"]
                except KeyError:
                    isbn = "-"
                try:
                    language = item["volumeInfo"]["language"]
                except KeyError:
                    language = "-"
                try:
                    front_page_link = item["volumeInfo"]["previewLink"]
                except KeyError:
                    front_page_link = "#"
                try:
                    page_count = item["volumeInfo"]["pageCount"]
                except KeyError:
                    page_count = "0"

                books_list_cleaned.append(
                    {
                        "title": title,
                        "author": author,
                        "publication_date": publication_date,
                        "isbn": isbn,
                        "language": language,
                        "front_page_link": front_page_link,
                        "page_count": page_count,
                    }
                )

            if request.GET.get("search"):  # only search for books
                return render(
                    request,
                    "main/import_books.html",
                    {"form": form, "books_list_cleaned": books_list_cleaned},
                )
            elif request.GET.get("save_book"):  # save selected book
                book_index = int(request.GET.get("save_book")) - 1
                title_var = books_list_cleaned[book_index]["title"]
                author_var = books_list_cleaned[book_index]["author"]
                publication_date_var = books_list_cleaned[book_index][
                    "publication_date"
                ]
                isbn_var = books_list_cleaned[book_index]["isbn"]
                page_count_var = books_list_cleaned[book_index]["page_count"]
                front_page_link_var = books_list_cleaned[book_index]["front_page_link"]
                language_var = books_list_cleaned[book_index]["language"]
                try:
                    _ = Books.objects.get(isbn=isbn_var)
                    messages.warning(request, "Wybrana książka jest już zapisana!")
                except KeyError:
                    try:
                        book = Books(
                            title=title_var,
                            author=author_var,
                            publication_date=publication_date_var,
                            isbn=isbn_var,
                            page_count=page_count_var,
                            front_page_link=front_page_link_var,
                            language=language_var,
                        )
                        book.save()
                        messages.success(
                            request,
                            'Pomyślnie dodano książkę "{}" {}!'.format(
                                title_var, author_var
                            ),
                        )
                    except KeyError:
                        messages.error(request, "Nie udało się dodać książki!")
                return render(
                    request,
                    "main/import_books.html",
                    {"form": form, "books_list_cleaned": books_list_cleaned},
                )
        else:
            form = ImportBooks()
            return render(request, "main/import_books.html", {"form": form})


@api_view(["GET"])
def api_overview(_):
    api_urls = {"List": "/book-list/", "Detail View": "/book-detail/<str:pk>/"}
    return Response(api_urls)


@api_view(["GET"])
def book_list(_):
    books = Books.objects.all().order_by("title")
    serializer = BooksSerializer(books, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def book_detail(request):
    books = Books.objects.all()

    for _ in request.GET:  # filtering api request
        title = request.GET.get("title")
        author = request.GET.get("author")
        language = request.GET.get("language")
        publication_date_after = request.GET.get("publication_date_after")
        publication_date_before = request.GET.get("publication_date_before")
        try:
            books = books.filter(title__contains=title)
        except ValueError:
            pass
        try:
            books = books.filter(author__contains=author)
        except ValueError:
            pass
        try:
            books = books.filter(language__contains=language)
        except ValueError:
            pass
        try:
            books = books.filter(publication_date__gte=publication_date_after)
        except ValueError:
            pass
        try:
            books = books.filter(publication_date__lte=publication_date_before)
        except ValueError:
            pass

    serializer = BooksSerializer(books, many=True)
    print(serializer.data)
    return Response(serializer.data)
