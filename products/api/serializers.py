from rest_framework.serializers import ModelSerializer
from ..models import Product

class ProductSerializer(ModelSerializer):
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'avatar', 
            'categories', 'created_time', 'updated_time',
        ]