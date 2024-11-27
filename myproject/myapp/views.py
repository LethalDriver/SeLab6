import json
from django.http import (
    JsonResponse,
    HttpResponseBadRequest,
    HttpResponseNotFound,
    HttpResponse,
)
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from decimal import Decimal
from django.core.exceptions import ValidationError


@csrf_exempt
def product_list(request):
    if request.method == "GET":
        products = list(Product.objects.values("id", "name", "price", "available"))
        return JsonResponse(products, safe=False)
    elif request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        price = data.get("price")
        available = data.get("available")

        if not name or price is None or available is None:
            return HttpResponseBadRequest("Missing required fields.")

        try:
            product = Product(name=name, price=Decimal(str(price)), available=available)
            product.full_clean()
            product.save()
            return JsonResponse(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "available": product.available,
                },
                status=201,
            )
        except ValidationError as e:
            return HttpResponseBadRequest(f"Validation error: {', '.join(e.messages)}")

    else:
        return HttpResponseBadRequest("Method not allowed.")


@csrf_exempt
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        if request.method == "GET":
            return JsonResponse(
                {
                    "id": product.id,
                    "name": product.name,
                    "price": float(product.price),
                    "available": product.available,
                }
            )
        else:
            return HttpResponseBadRequest("Method not allowed.")
    except Product.DoesNotExist:
        return HttpResponseNotFound("Product not found.")


# Create your views here.
def hello_world(request):
    return HttpResponse("Hello, World!")
