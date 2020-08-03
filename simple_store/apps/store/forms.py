from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(required=False)

    class Media:
        pass
