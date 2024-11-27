from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomerViewSet, OrderViewSet, ProductViewSet

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"orders", OrderViewSet, basename="order")

urlpatterns = [
    path("api/", include(router.urls)),
]
