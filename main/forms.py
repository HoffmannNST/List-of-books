from django import forms
from .models import Books


class BookHandler(forms.ModelForm):
    class Meta:
        model = Books
        fields = (
            "title",
            "author",
            "publication_date",
            "isbn",
            "page_count",
            "front_page_link",
            "language",
        )

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "tytuł..."}
            ),
            "author": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "autor..."}
            ),
            "publication_date": forms.DateInput(
                attrs={"class": "form-control mb-2", "placeholder": "RRRR-MM-DD"}
            ),
            "isbn": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "ISBN..."}
            ),
            "page_count": forms.NumberInput(
                attrs={"class": "form-control mb-2", "placeholder": "liczba stron..."}
            ),
            "front_page_link": forms.TextInput(
                attrs={
                    "class": "form-control mb-2",
                    "placeholder": "link do okładki...",
                }
            ),
            "language": forms.TextInput(
                attrs={
                    "class": "form-control mb-3",
                    "placeholder": "język publikacji...",
                }
            ),
        }

        labels = {
            "title": "Tytuł",
            "author": "Autor",
            "publication_date": "Data publikacji",
            "isbn": "ISBN",
            "page_count": "Liczba stron",
            "front_page_link": "Link do okładki",
            "language": "Język",
        }

    def clean(self):
        cleaned_data = super().clean()
        author = cleaned_data.get("author")
        page_count = cleaned_data.get("page_count")
        validation_error_list = []
        if len(author) < 2:
            validation_error_list.append("au_short")
        if page_count < 0:
            validation_error_list.append("pc_small")
        if len(validation_error_list) > 0:
            raise forms.ValidationError(validation_error_list)


class ImportBooks(forms.Form):
    import_key_words = forms.CharField(
        label="Słowa kluczowe",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Szukana książka...",
                "style": "text-align:left;",
            }
        ),
    )
