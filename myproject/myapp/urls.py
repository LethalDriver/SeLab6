from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CustomerViewSet,
    OrderViewSet,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductViewSet,
)

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("user/products/", ProductListView.as_view(), name="product_list"),
    path("user/products/<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path("user/products/new/", ProductCreateView.as_view(), name="product_create"),
    path("api/", include(router.urls)),
]
