from django.urls import path
from . import views

urlpatterns = [
    path("<int:item_id>/", views.book_data, name="book_data"),
    path("list_of_books/", views.list_of_books, name="list_of_books"),
    path("edit/<int:item_id>/", views.edit, name="edit"),
    path("import_books/", views.import_books, name="import_books"),
    path("api-overview/", views.apiOverview, name="api_overview"),
    path("book-list/", views.bookList, name="book_list"),
    path("book-detail/<str:pk>/", views.bookDetail, name="book_detail"),
]
