from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Category, Product, File
from .serializers import CategorySerializer, ProductSerializer, FileSerializer

# Create your views here.
class ProductlistView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)