import django_filters
from django import forms
from .models import Books
from django_filters import CharFilter, DateFilter


class BooksFilter(django_filters.FilterSet):
    title = CharFilter(
        field_name="title",
        lookup_expr="contains",
        label="Tytuł",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Szukany tytuł...",
                "style": "text-align:left;",
            }
        ),
    )

    author = CharFilter(
        field_name="author",
        lookup_expr="contains",
        label="Autor",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Szukany autor...",
                "style": "text-align:left;",
            }
        ),
    )

    language = CharFilter(
        field_name="language",
        lookup_expr="contains",
        label="Język",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Szukany język...",
                "style": "text-align:left;",
            }
        ),
    )

    start_date = DateFilter(
        field_name="publication_date",
        lookup_expr="gte",
        label="Data od",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "RRRR-MM-DD",
                "style": "text-align:left;",
            }
        ),
    )

    end_date = DateFilter(
        field_name="publication_date",
        lookup_expr="lte",
        label="Data do",
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "placeholder": "RRRR-MM-DD",
                "style": "text-align:left;",
            }
        ),
    )

    class Meta:
        model = Books
        fields = []
