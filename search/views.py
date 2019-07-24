from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from search.search_form import SearchForm
from django.contrib.auth.decorators import login_required
from stop_words import get_stop_words
from django.db.models import Q
from random import randrange

from .models import Product
from core.models import CustomUser

# Create your views here.


def index(request):
    if request.method == "POST":
        print("post")
        # form object instanciation with data  from requested object
        form = SearchForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["post"].casefold()
            stop_words = get_stop_words("fr")
            splited_search = data.split(" ")
            resulting_search = list(set(splited_search) - set(stop_words))

            db_res = words_filter(resulting_search)
            res = [i for i in db_res]

            print(res)
            context = {"form": form, "res": res}
            return render(request, "search/index.html", context)

    form = SearchForm()
    return render(request, "search/index.html", {"form": form})


def words_filter(resulting_search):
    """ filter the number of words in search with AND """

    if len(resulting_search) < 2:
        result = Product.objects.filter(product_name__contains=resulting_search[0])
        return result
    elif len(resulting_search) < 3:
        result = Product.objects.filter(
            product_name__contains=resulting_search[0]
        ).filter(product_name__contains=resulting_search[1])
        return result
    elif len(resulting_search) < 4:
        result = (
            Product.objects.filter(product_name__contains=resulting_search[0])
            .filter(product_name__contains=resulting_search[1])
            .filter(product_name__contains=resulting_search[2])
        )
        return result
    elif len(resulting_search) < 5:
        result = (
            Product.objects.filter(product_name__contains=resulting_search[0])
            .filter(product_name__contains=resulting_search[1])
            .filter(product_name__contains=resulting_search[2])
            .filter(product_name__contains=resulting_search[3])
        )
        return result


def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    print(product.product_image)
    json_data = {
        "product": product,
        "code": product.product_code,
        "nova_groups": product.nova_groups,
        "categories": product.categories,
        "nutriscore": product.nutriscore.capitalize(),
        "image": product.product_image,
        "fat_100g": product.fat_100g,
        "salt_100g": product.salt_100g,
        "saturated_fat_100g": product.saturated_fat_100g,
        "sugars_100g": product.sugars_100g,
    }
    return render(request, "search/detail.html", json_data)


def mentions(request):
    return render(request, "search/mentions_legales.html")


def swap(request, product_id):
    """
    get categories form request
    search database for products matching all categories
    and with nutriscore corresponding to A
    display food product
    """

    product = get_object_or_404(Product, pk=product_id)
    splited = product.categories.split(",")
    #trick to avoid products with less than 3 categories
    if len(splited) < 3:
        splited.append(" x")

    categories_res = (
        Product.objects.filter(categories__contains=splited[0])
        .filter(categories__contains=splited[1])
        .filter(categories__contains=splited[2])
        .filter(nutriscore__lt=product.nutriscore)
    )  # order_by(?) + slice sur le 1er
    # print(categories_res)
    # print(product.nutriscore)
    arr = []
    for x in categories_res:
        z = compare_products(x, product)
        if z is not None:
            arr.append(z)

    if bool(arr) is False:
        substitute = product
        json_data = {
            "product": substitute,
            "code": substitute.product_code,
            "nova_groups": substitute.nova_groups,
            "categories": substitute.categories,
            "nutriscore": substitute.nutriscore.capitalize(),
            "image": substitute.product_image,
            "status": "Pas de meilleur produit trouvé !",
            "id": product_id,
        }
    else:
        substitute = arr[randrange(len(arr))][
            0
        ]  # select substitute randomly among all better products
        # print(substitute.product_code)
        json_data = {
            "product": substitute,
            "code": substitute.product_code,
            "nova_groups": substitute.nova_groups,
            "categories": substitute.categories,
            "nutriscore": substitute.nutriscore.capitalize(),
            "image": substitute.product_image,
            "status": "",
            "id": product_id,
        }

    return render(request, "search/swap.html", json_data)


def compare_products(x, y):
    """ compare nutriscores to return better product"""

    abc = ["a", "b", "c", "d", "e", "f", "g"]
    # if x location's index in abc is lower than y location's index then...
    better = abc.index(x.nutriscore)
    original = abc.index(y.nutriscore)

    if better < original:
        # print("better product")
        return x, x.id


@login_required
def list_products(request):
    current_user = request.user

    context = get_substitutes(current_user)

    return render(request, "search/list_products.html", context)


# @login_required
def add_substitute(request, product_id, subs_id):

    current_user = request.user

    # add current substitute to current_user using fk relation
    product_to_associate = Product.objects.get(id=product_id)  # to delete
    user_to_associate = CustomUser.objects.get(email=current_user)
    user_to_associate.user_substitutes.add(subs_id)

    context = get_substitutes(current_user)

    return render(request, "search/list_products.html", context)


# @login_required
def get_substitutes(current_user):
    # redirect to substitute list of connected user
    substitutes_list = CustomUser.objects.filter(user_substitutes__isnull=False).filter(
        email=current_user
    )

    if not substitutes_list:
        return None
    else:
        main_sub_list = [i for i in substitutes_list]
        sub_list = [j for j in main_sub_list[0].user_substitutes.all()]

        context = {"full_list": sub_list}

        return context


@login_required
def remove_substitute(request, product_id):

    current_user = request.user

    user_to_associate = CustomUser.objects.get(email=current_user)
    user_to_associate.user_substitutes.remove(product_id)

    context = get_substitutes(current_user)

    return render(request, "search/list_products.html", context)

