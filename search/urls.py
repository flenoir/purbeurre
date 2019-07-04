from django.urls import path

from . import views


app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:product_id>/', views.detail, name='detail'),
    path('swap/<int:product_id>/', views.swap, name='swap'),   
    path('list_products/', views.list_products, name='list_products'),
    path('add_substitute/<int:product_id>/<int:subs_id>/', views.add_substitute, name='add_substitute')
]