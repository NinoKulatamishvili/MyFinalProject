from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Products
from .serializer import ProductsSerializer



@api_view(['GET'])
def get_routes(request):
    routes = [
        "GET /api",
        "GET /api/products",
        "GET /api/product/:id"
    ]
    return Response(routes)

@api_view(['GET'])
def get_products(request):
    products = Products.objects.all()
    serializer = ProductsSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_product(request, id):
    product = Products.objects.get(id=id)
    serializer = ProductsSerializer(product, many=False)
    return Response(serializer.data)

