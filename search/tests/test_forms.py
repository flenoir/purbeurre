from django.test import TestCase
from search.search_form import SearchForm


class FormTests(TestCase):
    # test form is valid
    def test_form_is_valid(self):
        form_data = {"post": "poulet aux brocolis"}
        form = SearchForm(form_data)
        self.assertTrue(form.is_valid())

