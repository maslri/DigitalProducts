from .views import (
    ProductlistView, ProductDetailView, CategorylistView, CategoryDetailView, FilelistView, FileDetailView
)
from django.urls import path

urlpatterns = [
    path('categories/', CategorylistView.as_view(), name='categories'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),

    path('products/', ProductlistView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

    path('products/<int:product_pk>/files/', FilelistView.as_view(), name='files'),
    path('products/<int:product_pk>/files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
]
