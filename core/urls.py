from django.urls import path, include

from .views import SignupView


urlpatterns = [
    path('', SignupView.as_view(), name='signup'),
]