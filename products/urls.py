from .views import ProductlistView
from django.urls import path

urlpatterns = [
    path('products/', ProductlistView.as_view(), name='products'),
]
