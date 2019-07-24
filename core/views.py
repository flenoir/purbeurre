from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from search.search_form import SearchForm

# Create your views here.


def home(request):
    form = SearchForm()
    return render(request, "search/index.html", {"form": form})


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})
