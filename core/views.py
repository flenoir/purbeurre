from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from search.search_form import SearchForm
from django.views.generic.edit import FormView

# Create your views here.


def home(request):
    form = SearchForm()
    # return render(request, "search/index.html", {"form": form})
    return redirect("search/")


class SignupView(FormView):
    form_class = UserCreationForm
    template_name = "account/signup.html"
