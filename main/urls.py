from django.urls import path, re_path
from . import views

urlpatterns = [
    path("list_of_books/", views.list_of_books, name="list_of_books"),
    path("edit/<int:item_id>/", views.edit, name="edit"),
    path("import_books/", views.import_books, name="import_books"),
    path("api-overview/", views.api_overview, name="api_overview"),
    path("book-list/", views.book_list, name="book_list"),
    re_path(r"^book-detail/", views.book_detail, name="book_detail"),
]
