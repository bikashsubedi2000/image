# imageresizer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.resize_image, name='resize_image'),
]