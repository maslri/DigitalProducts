from rest_framework.routers import DefaultRouter
from products.api.urls import product_router
from django.urls import path, include

router = DefaultRouter()
# product
router.registry.extend(product_router.registry)

urlpatterns = [
    path('api/', include(router.urls))
]
