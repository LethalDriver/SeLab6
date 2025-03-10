from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter

from .views import (
    CustomerViewSet,
    OrderViewSet,
    ProductCreateView,
    ProductDetailView,
    ProductListView,
    ProductViewSet,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Software engineering lab",
        default_version="v1",
        description="API documentation for the lab",
    ),
    public=True,
    permission_classes=(AllowAny,),
    authentication_classes=[],
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
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]
