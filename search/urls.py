from django.urls import path

from . import views


app_name = "search"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:product_code>/", views.detail, name="detail"),
    path("swap/<int:product_code>/", views.swap, name="swap"),
    path("remove/<int:product_code>/", views.remove_substitute, name="remove"),
    path("list_products/", views.list_products, name="list_products"),
    path(
        "add_substitute/<int:product_code>/<int:subs_id>/",
        views.add_substitute,
        name="add_substitute",
    ),
    path("mentions_legales/", views.mentions, name="mentions"),
]
