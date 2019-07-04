from django import forms

class SearchForm(forms.Form):
    post = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Produit', 'size': '80'}))